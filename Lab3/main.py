# -*- coding: utf-8 -*-
"""SE373 - BTVN3 - Triển khai Agent Đặt Vé Máy Bay bằng 3 mẫu thiết kế khác nhau (ReAct, Plan-then-Execute, Hybrid).

Thực thi:
    python main.py --pattern react --scenario chuan
    python main.py --pattern plan-execute --scenario chuan
    python main.py --pattern hybrid --scenario chuan

Kịch bản:
    --scenario chuan       : Luồng bình thường, thành công
    --scenario lap         : Phát hiện vòng lặp
    --scenario vuot-gia    : Ngân sách bị vượt, cần xử lý handoff
    --scenario can-duyet   : Vé nhạy cảm, chờ người duyệt
    --scenario ao-giac     : Dữ liệu ảo, GroundingVerifier bắt lỗi

Sử dụng LLM thật:
    python main.py --pattern react --real
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional

from lib.mock_flight_db import mock_db
from lib.harness import BookingConstraints, HandoffManager, PermissionGuard
from lib.model_gia import ModelGiaFlight, model_that
from lib.agent_react import ReActFlightAgent
from lib.agent_plan_execute import PlanThenExecuteFlightAgent
from lib.agent_hybrid import HybridFlightAgent

DEFAULT_QUERY = (
    "Tôi cần đặt 1 vé máy bay từ TP.HCM đi Phú Quốc, bay sáng 2026-12-20, "
    "ngân sách tầm 2.000.000 VNĐ. Tên tôi: Đinh Nguyễn Đức Tâm, CCCD: 079201009999."
)

def run_agent_workflow(
    pattern: str,
    scenario: str = "chuan",
    use_real_model: bool = False,
    auto_approve: bool = False,
    query: Optional[str] = None,
) -> dict:
    """Thực thi Agent với cấu hình cho trước."""
    mock_db.reset()

    is_over_budget = scenario in ["vuot-gia", "vuot_gia"]
    budget_limit = 1200000 if is_over_budget else 2000000

    if not query:
        if is_over_budget:
            query = (
                "Tôi cần đặt 1 vé máy bay từ TP.HCM đi Phú Quốc, bay sáng 2026-12-20, "
                "ngân sách tầm 1.200.000 VNĐ. Tên tôi: Đinh Nguyễn Đức Tâm, CCCD: 079201009999."
            )
        else:
            query = DEFAULT_QUERY

    # Khởi tạo ràng buộc
    flight_constraints = BookingConstraints(
        origin="SGN",
        destination="PQC",
        depart_date="2026-12-20",
        time_window="sang",
        max_price=budget_limit,
        passenger_name="Đinh Nguyễn Đức Tâm",
        passenger_id="079201009999",
    )

    # Chọn LLM
    if use_real_model:
        try:
            model = model_that()
            print(">>> Sử dụng LLM cấu hình từ môi trường (.env)")
        except Exception as err:
            print(f"[WARN] Lỗi tải LLM thật ({err}). Dùng ModelGiaFlight thay thế.")
            model = ModelGiaFlight(kich_ban=scenario)
    else:
        model = ModelGiaFlight(kich_ban=scenario)

    # Khởi tạo kiểm duyệt
    security_guard = PermissionGuard(
        autopay_limit=1500000,
        auto_approve_test=(auto_approve or scenario == "chuan"),
    )

    print("=" * 70)
    print(f"HỆ THỐNG AGENT ĐẶT VÉ MÁY BAY | PATTERN: {pattern.upper()} | SCENARIO: {scenario}")
    print("=" * 70)
    print(f"User Request: {query}")
    print(f"Constraints : {flight_constraints.origin} -> {flight_constraints.destination} | {flight_constraints.depart_date} ({flight_constraints.time_window}) | Max {flight_constraints.max_price:,} VNĐ")
    print("-" * 70)

    agent = None
    if pattern == "react":
        agent = ReActFlightAgent(model=model, constraints=flight_constraints, permission_guard=security_guard)
    elif pattern == "plan-execute":
        agent = PlanThenExecuteFlightAgent(model=model, constraints=flight_constraints, permission_guard=security_guard)
    elif pattern == "hybrid":
        agent = HybridFlightAgent(model=model, constraints=flight_constraints, permission_guard=security_guard)
    else:
        raise ValueError(f"Pattern '{pattern}' không được hỗ trợ.")

    result = agent.run(query)

    print("\n--- TRACE HÀNH ĐỘNG ---")
    for i, action in enumerate(result.get("executed_actions", []), 1):
        print(f" -> Bước {i}: Gọi Tool {action}")

    print("\n--- KẾT QUẢ ĐÁNH GIÁ HARNESS ---")
    print(f"- Trạng thái      : {result.get('status')}")
    print(f"- Số bước         : {result.get('steps')}")
    print(f"- Tổng Tokens     : {result.get('total_tokens')}")
    print(f"- Thời gian (s)   : {result.get('elapsed_time')}s")

    # Kiểm tra bằng code (Lớp 2)
    comp_metrics = result.get("completion_report", {})
    if comp_metrics:
        print("\n[Harness Lớp 2: Kiểm tra Hoàn thành]:")
        print(f"  > Trạng thái hoàn thành: {comp_metrics.get('is_completed')}")
        for check, passed in comp_metrics.get("checks", {}).items():
            print(f"    - {check:25}: {'[OK]' if passed else '[FAILED]'}")

    # Chống ảo giác (Lớp 1)
    gr_metrics = result.get("grounding_report", {})
    if gr_metrics:
        print("\n[Harness Lớp 1: Chống Ảo Giác]:")
        is_safe = gr_metrics.get('passed')
        print(f"  > Căn cứ hợp lệ : {'[OK] Dữ liệu chuẩn' if is_safe else '[FAILED] CÓ SỰ BỊA ĐẶT'}")
        if not is_safe:
            print(f"  > Chi tiết lỗi  : {gr_metrics.get('ungrounded_facts')}")

    # Handoff (Lớp 4)
    handoff_info = result.get("handoff_report")
    if handoff_info:
        print("\n" + HandoffManager.format_handoff_display(handoff_info))
    else:
        print("\n--- KẾT QUẢ TRẢ VỀ CHO USER ---")
        print(result.get("final_response"))

    print("=" * 70 + "\n")
    return result

def main():
    parser = argparse.ArgumentParser(description="Chương trình thử nghiệm Agent Đặt Vé")
    parser.add_argument("--pattern", default="react", choices=["react", "plan-execute", "hybrid", "all"], help="Mẫu thiết kế Agent")
    parser.add_argument("--scenario", default="chuan", choices=["chuan", "lap", "vuot-gia", "can-duyet", "ao-giac"], help="Kịch bản giả lập")
    parser.add_argument("--real", action="store_true", help="Chạy với model LLM thật")
    parser.add_argument("--auto-approve", action="store_true", help="Tự động đồng ý khi yêu cầu duyệt")

    args = parser.parse_args()

    if args.pattern == "all":
        print("\n[KIỂM THỬ TẤT CẢ CÁC MẪU THIẾT KẾ]\n")
        for p in ["react", "plan-execute", "hybrid"]:
            run_agent_workflow(pattern=p, scenario=args.scenario, use_real_model=args.real, auto_approve=args.auto_approve)
    else:
        run_agent_workflow(pattern=args.pattern, scenario=args.scenario, use_real_model=args.real, auto_approve=args.auto_approve)

if __name__ == "__main__":
    sys.exit(main())

