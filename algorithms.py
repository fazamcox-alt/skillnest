# algorithms.py
from datetime import date, timedelta
from typing import Dict, Any, List


def check_and_lock_batch(student_count: int, max_seats: int = 20) -> Dict[str, Any]:
    """
    ব্যাচে শিক্ষার্থীর সংখ্যা নির্ধারিত সীমাতে (২০ জন) পৌঁছালে
    স্বয়ংক্রিয়ভাবে ব্যাচ লক করার স্ট্যাটাস প্রদান করে।
    """
    is_locked = student_count >= max_seats
    available_seats = max(0, max_seats - student_count)

    return {
        "student_count": student_count,
        "max_seats": max_seats,
        "is_locked": is_locked,
        "available_seats": available_seats,
        "status_message": "Batch is Full & Locked." if is_locked else f"{available_seats} seats remaining."
    }


def calculate_teacher_commission(
        base_commission_percent: float = 30.0,
        ai_engagement_score: float = 0.0,  # ০ থেকে ১০ এর স্কেলে
        student_satisfaction_rating: float = 0.0  # ০ থেকে ৫ এর স্কেলে
) -> Dict[str, Any]:
    """
    টিচারের ডায়নামিক কমিশন হিসাব করে।
    বেস ৩০% + এআই এনগেজমেন্ট বোনাস (সর্বোচ্চ ১০%) + স্টুডেন্ট রেটিং বোনাস (সর্বোচ্চ ১০%)
    সর্বোচ্চ কমিশন ক্যাপ ৫০%।
    """
    # এআই স্কোর কনভার্শন (১০ এর মধ্যে স্কোরের সমপরিমাণ পার্সেন্টেজ বোনাস)
    ai_bonus = min(10.0, max(0.0, ai_engagement_score))

    # স্টুডেন্ট স্যাটিসফ্যাকশন কনভার্শন (৫ এর স্কেলকে ডাবল করে ১০% এ রূপান্তর)
    rating_bonus = min(10.0, max(0.0, student_satisfaction_rating * 2.0))

    total_commission_percent = min(50.0, base_commission_percent + ai_bonus + rating_bonus)

    return {
        "base_commission_percent": base_commission_percent,
        "ai_bonus_percent": round(ai_bonus, 2),
        "rating_bonus_percent": round(rating_bonus, 2),
        "final_commission_percent": round(total_commission_percent, 2)
    }


def verify_refund_eligibility(
        total_classes: int,
        attended_classes: int,
        total_weekly_videos_required: int,
        submitted_weekly_videos: int,
        daily_practice_logs_count: int,
        days_enrolled: int
) -> Dict[str, Any]:
    """
    রিফান্ড পলিসির অপব্যবহার রোধে অ্যালগরিদমিক অডিট গেট।
    শর্ত:
    ১. উপস্থিতি ন্যূনতম ৮০% হতে হবে।
    ২. সবকটি সাপ্তাহিক ভিডিও জমা থাকতে হবে।
    ৩. অন্তত ৭০% দিনের লাইফ-লগ ডাটা থাকতে হবে।
    """
    attendance_rate = (attended_classes / total_classes * 100) if total_classes > 0 else 0.0
    video_completion_rate = (
                submitted_weekly_videos / total_weekly_videos_required * 100) if total_weekly_videos_required > 0 else 0.0
    log_consistency_rate = (daily_practice_logs_count / days_enrolled * 100) if days_enrolled > 0 else 0.0

    meets_attendance = attendance_rate >= 80.0
    meets_videos = submitted_weekly_videos >= total_weekly_videos_required
    meets_logs = log_consistency_rate >= 70.0

    is_eligible = meets_attendance and meets_videos and meets_logs

    reasons = []
    if not meets_attendance:
        reasons.append(f"Attendance is {round(attendance_rate, 1)}% (Minimum 80% required).")
    if not meets_videos:
        reasons.append(f"Submitted {submitted_weekly_videos}/{total_weekly_videos_required} weekly videos.")
    if not meets_logs:
        reasons.append(f"Life-log submitted for {round(log_consistency_rate, 1)}% days (Minimum 70% required).")

    return {
        "is_eligible_for_refund": is_eligible,
        "attendance_rate": round(attendance_rate, 1),
        "video_completion_rate": round(video_completion_rate, 1),
        "log_consistency_rate": round(log_consistency_rate, 1),
        "rejection_reasons": reasons if not is_eligible else []
    }