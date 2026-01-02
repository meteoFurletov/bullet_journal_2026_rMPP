import os
import calendar
from datetime import date, timedelta
import config
from src.infrastructure.pdf_adapter import FPDFAdapter
from src.logic.journal_map import NavigationSpine
from src.workers.grid_worker import GridInput
from src.workers.daily_worker import DailyWorker, DailyInput
from src.workers.weekly_worker import WeeklyWorker, WeeklyInput
from src.workers.monthly_worker import MonthlyWorker, MonthlyInput
from src.workers.index_worker import IndexWorker, IndexInput


def main():
    # 1. Setup PDF
    pdf = FPDFAdapter(format=(config.CANVAS_WIDTH, config.CANVAS_HEIGHT))

    # Load Fonts
    if os.path.exists(config.FONT_REGULAR):
        pdf.add_font(config.FONT_NAME, "", config.FONT_REGULAR)
    if os.path.exists(config.FONT_BOLD):
        pdf.add_font(config.FONT_NAME, "B", config.FONT_BOLD)
    if os.path.exists(config.FONT_ITALIC):
        pdf.add_font(config.FONT_NAME, "I", config.FONT_ITALIC)

    # 2. Date Logic
    target_year = 2026
    jan_one = date(target_year, 1, 1)
    start_date = jan_one - timedelta(days=jan_one.weekday())
    total_weeks = 53

    # 3. Navigation Spine (Pass 1: Create Links and assign destinations)
    spine = NavigationSpine(pdf)
    journal_map = spine.initialize_links(start_date, total_weeks, target_year)

    # 4. Initialize Workers
    grid_input = GridInput(
        canvas_width=config.CANVAS_WIDTH,
        canvas_height=config.CANVAS_HEIGHT,
        grid_size=config.GRID_SIZE,
        toolbar_buffer=config.TOOLBAR_BUFFER,
        dot_radius=config.DOT_RADIUS,
    )

    daily_worker = DailyWorker(pdf)
    weekly_worker = WeeklyWorker(pdf)
    monthly_worker = MonthlyWorker(pdf)
    index_worker = IndexWorker(pdf)

    # 5. Generation Loop

    # --- A. Index Pages ---
    unique_months = []
    for i in range(total_weeks):
        d = start_date + timedelta(weeks=i)
        if d.year < target_year:
            continue
        m_key = (d.year, d.month)
        if m_key not in unique_months:
            unique_months.append(m_key)

    month_links = [
        (calendar.month_name[m[1]], journal_map.month_timeline_links[m])
        for m in unique_months
    ]

    week_links = []
    for w in range(1, total_weeks + 1):
        monday = start_date + timedelta(weeks=w - 1)
        sunday = monday + timedelta(days=6)
        label = f"W{w}: {monday.strftime('%b %d')} - {sunday.strftime('%b %d')}"
        week_links.append((label, journal_map.week_action_links[w]))

    daily_links_data = []
    for year, month in unique_months:
        month_name = calendar.month_name[month]
        days_in_month = calendar.monthrange(year, month)[1]
        days = []
        for day in range(1, days_in_month + 1):
            days.append((day, journal_map.day_links[(year, month, day)]))
        daily_links_data.append((month_name, year, days))

    index_input = IndexInput(
        start_date=start_date,
        total_weeks=total_weeks,
        grid_input=grid_input,
        month_links=month_links,
        week_links=week_links,
        daily_links=daily_links_data,
    )

    index_worker.draw_months_and_weeks(index_input)
    index_worker.draw_daily_logs(index_input)

    # --- B. Content Pages ---
    last_month_key = None

    for week_num in range(1, total_weeks + 1):
        current_monday = start_date + timedelta(weeks=week_num - 1)
        month_key = (current_monday.year, current_monday.month)

        # Monthly Pages
        if month_key != last_month_key and month_key in unique_months:
            month_name = calendar.month_name[current_monday.month]
            days_in_month = calendar.monthrange(
                current_monday.year, current_monday.month
            )[1]

            prev_month_key = (
                unique_months[unique_months.index(month_key) - 1]
                if unique_months.index(month_key) > 0
                else None
            )
            next_month_key = (
                unique_months[unique_months.index(month_key) + 1]
                if unique_months.index(month_key) < len(unique_months) - 1
                else None
            )

            nav_links = [
                ("Index", journal_map.index_link),
                ("Prev month", journal_map.month_timeline_links.get(prev_month_key)),
                ("Next month", journal_map.month_timeline_links.get(next_month_key)),
            ]

            day_links = [
                journal_map.day_links[(current_monday.year, current_monday.month, d)]
                for d in range(1, days_in_month + 1)
            ]

            monthly_worker.draw_timeline(
                MonthlyInput(
                    month_name=month_name,
                    month=current_monday.month,
                    year=current_monday.year,
                    days_in_month=days_in_month,
                    instructions=config.TEXT_TIMELINE,
                    nav_links=nav_links,
                    grid_input=grid_input,
                    day_links=day_links,
                )
            )

            nav_links_action = [
                ("Index", journal_map.index_link),
                ("Prev month", journal_map.month_action_links.get(prev_month_key)),
                ("Next month", journal_map.month_action_links.get(next_month_key)),
            ]

            monthly_worker.draw_action_plan(
                MonthlyInput(
                    month_name=month_name,
                    month=current_monday.month,
                    year=current_monday.year,
                    days_in_month=days_in_month,
                    instructions=config.TEXT_MONTHLY_ACTION,
                    nav_links=nav_links_action,
                    grid_input=grid_input,
                    day_links=[],
                )
            )

            last_month_key = month_key

        # Weekly Action Plan
        week_end = current_monday + timedelta(days=6)
        date_str = (
            f"{current_monday.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}"
        )

        nav_links_week = [
            ("Index", journal_map.index_link),
            ("Prev week", journal_map.week_action_links.get(week_num - 1)),
            ("Next week", journal_map.week_action_links.get(week_num + 1)),
        ]

        weekly_worker.draw_action_plan(
            WeeklyInput(
                date_str=date_str,
                nav_links=nav_links_week,
                grid_input=grid_input,
                instructions=config.TEXT_ACTION_PLAN,
            )
        )

        # Daily Pages
        for day_offset in range(7):
            day_date = current_monday + timedelta(days=day_offset)

            m_key = (day_date.year, day_date.month)

            nav_links_day = [
                ("Index", journal_map.index_link),
                ("Monthly log", journal_map.month_timeline_links.get(m_key)),
                ("Weekly log", journal_map.week_action_links[week_num]),
            ]

            daily_worker.draw_page(
                DailyInput(
                    day_date=day_date, nav_links=nav_links_day, grid_input=grid_input
                )
            )

        # Weekly Reflection
        weekly_worker.draw_reflection(
            WeeklyInput(
                date_str=date_str,
                nav_links=nav_links_week,
                grid_input=grid_input,
                instructions=config.TEXT_REFLECTION,
            )
        )

    # 6. Output
    pdf.output("output/bujo_2026.pdf")
    print("PDF Generated: output/bujo_2026.pdf")


if __name__ == "__main__":
    main()
