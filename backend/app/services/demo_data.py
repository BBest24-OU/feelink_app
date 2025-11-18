"""
Demo Data Service - Generate and clear demo data
"""
from datetime import date, timedelta
from typing import Dict, Any
import random
from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy import delete

from app.models import User, Metric, Entry, EntryValue


class DemoDataService:
    """Service for managing demo data generation and clearing"""

    DEMO_METRICS = [
        # Physical metrics
        {
            "name_key": "sleep_hours",
            "category": "physical",
            "value_type": "range",
            "min_value": 0,
            "max_value": 12,
            "description": "Hours of sleep",
            "color": "#3B82F6",
            "icon": "moon"
        },
        {
            "name_key": "sleep_quality",
            "category": "physical",
            "value_type": "range",
            "min_value": 1,
            "max_value": 10,
            "description": "Quality of sleep (1-10)",
            "color": "#60A5FA",
            "icon": "star"
        },
        {
            "name_key": "energy_level",
            "category": "physical",
            "value_type": "range",
            "min_value": 1,
            "max_value": 10,
            "description": "Energy level (1-10)",
            "color": "#FBBF24",
            "icon": "battery"
        },
        {
            "name_key": "headache",
            "category": "physical",
            "value_type": "boolean",
            "description": "Experienced headache",
            "color": "#EF4444",
            "icon": "alert"
        },
        {
            "name_key": "exercise_minutes",
            "category": "physical",
            "value_type": "number",
            "description": "Minutes of exercise",
            "color": "#10B981",
            "icon": "activity"
        },
        # Psychological metrics
        {
            "name_key": "mood",
            "category": "psychological",
            "value_type": "range",
            "min_value": 1,
            "max_value": 10,
            "description": "Overall mood (1-10)",
            "color": "#8B5CF6",
            "icon": "smile"
        },
        {
            "name_key": "anxiety_level",
            "category": "psychological",
            "value_type": "range",
            "min_value": 1,
            "max_value": 10,
            "description": "Anxiety level (1-10)",
            "color": "#F59E0B",
            "icon": "alert-circle"
        },
        {
            "name_key": "stress_level",
            "category": "psychological",
            "value_type": "range",
            "min_value": 1,
            "max_value": 10,
            "description": "Stress level (1-10)",
            "color": "#DC2626",
            "icon": "zap"
        },
        {
            "name_key": "motivation",
            "category": "psychological",
            "value_type": "range",
            "min_value": 1,
            "max_value": 10,
            "description": "Motivation level (1-10)",
            "color": "#06B6D4",
            "icon": "trending-up"
        },
        {
            "name_key": "social_interaction",
            "category": "psychological",
            "value_type": "boolean",
            "description": "Had social interaction",
            "color": "#EC4899",
            "icon": "users"
        },
        # Medications
        {
            "name_key": "morning_medication",
            "category": "medications",
            "value_type": "boolean",
            "description": "Took morning medication",
            "color": "#14B8A6",
            "icon": "pill"
        },
        {
            "name_key": "evening_medication",
            "category": "medications",
            "value_type": "boolean",
            "description": "Took evening medication",
            "color": "#0EA5E9",
            "icon": "pill"
        },
        # Self-care
        {
            "name_key": "meditation",
            "category": "selfcare",
            "value_type": "number",
            "description": "Minutes of meditation",
            "color": "#A855F7",
            "icon": "sun"
        },
        {
            "name_key": "journaling",
            "category": "selfcare",
            "value_type": "boolean",
            "description": "Did journaling",
            "color": "#6366F1",
            "icon": "book"
        },
        {
            "name_key": "water_intake",
            "category": "wellness",
            "value_type": "count",
            "description": "Glasses of water (count)",
            "color": "#0284C7",
            "icon": "droplet"
        },
        # Triggers
        {
            "name_key": "caffeine_intake",
            "category": "triggers",
            "value_type": "count",
            "description": "Cups of coffee/tea",
            "color": "#92400E",
            "icon": "coffee"
        },
        {
            "name_key": "alcohol",
            "category": "triggers",
            "value_type": "boolean",
            "description": "Consumed alcohol",
            "color": "#B91C1C",
            "icon": "wine"
        },
        {
            "name_key": "screen_time",
            "category": "triggers",
            "value_type": "number",
            "description": "Hours of screen time",
            "color": "#4B5563",
            "icon": "monitor"
        }
    ]

    @classmethod
    def generate_demo_data(cls, db: Session, user: User) -> Dict[str, Any]:
        """
        Generate demo data for the user for the last 180 days.

        Args:
            db: Database session
            user: User to generate data for

        Returns:
            Summary of generated data
        """
        # Create metrics
        metrics_created = []
        for metric_data in cls.DEMO_METRICS:
            # Check if metric already exists
            existing_metric = db.query(Metric).filter(
                Metric.user_id == user.id,
                Metric.name_key == metric_data["name_key"]
            ).first()

            if not existing_metric:
                metric = Metric(
                    user_id=user.id,
                    **metric_data
                )
                db.add(metric)
                metrics_created.append(metric)

        db.flush()  # Flush to get metric IDs

        # If no new metrics were created, get existing ones
        if not metrics_created:
            metrics_created = db.query(Metric).filter(Metric.user_id == user.id).all()

        # Generate entries for the last 180 days
        end_date = date.today()
        start_date = end_date - timedelta(days=179)

        entries_created = 0
        values_created = 0

        current_date = start_date
        while current_date <= end_date:
            # Skip some days randomly (simulate realistic usage - not every day)
            if random.random() > 0.85:  # 15% chance to skip a day
                current_date += timedelta(days=1)
                continue

            # Check if entry already exists for this date
            existing_entry = db.query(Entry).filter(
                Entry.user_id == user.id,
                Entry.entry_date == current_date
            ).first()

            if existing_entry:
                current_date += timedelta(days=1)
                continue

            # Create entry
            entry = Entry(
                user_id=user.id,
                entry_date=current_date,
                notes=cls._generate_note(current_date) if random.random() > 0.7 else None
            )
            db.add(entry)
            db.flush()  # Flush to get entry ID
            entries_created += 1

            # Add values for metrics (not all metrics every day)
            for metric in metrics_created:
                # 70-90% chance to track each metric on any given day
                if random.random() > 0.25:
                    value = cls._generate_metric_value(metric, current_date)
                    if value:
                        entry_value = EntryValue(
                            entry_id=entry.id,
                            metric_id=metric.id,
                            **value
                        )
                        db.add(entry_value)
                        values_created += 1

            current_date += timedelta(days=1)

        db.commit()

        return {
            "message": "Demo data generated successfully",
            "metrics_created": len(metrics_created),
            "entries_created": entries_created,
            "values_created": values_created,
            "date_range": {
                "start": str(start_date),
                "end": str(end_date)
            }
        }

    @classmethod
    def _generate_metric_value(cls, metric: Metric, entry_date: date) -> Dict[str, Any]:
        """
        Generate a realistic value for a metric.

        Args:
            metric: Metric to generate value for
            entry_date: Date of the entry

        Returns:
            Dictionary with value field(s)
        """
        # Add some variation based on day of week
        day_of_week = entry_date.weekday()
        is_weekend = day_of_week >= 5

        if metric.value_type == "range":
            # Generate values with realistic patterns
            if metric.name_key == "sleep_hours":
                # More sleep on weekends
                base = 7.5 if is_weekend else 7.0
                value = base + random.uniform(-1.5, 1.5)
                value = max(float(metric.min_value), min(float(metric.max_value), value))
            elif metric.name_key == "sleep_quality":
                # Quality correlated with hours (simple simulation)
                value = random.uniform(5.0, 9.0)
            elif metric.name_key == "energy_level":
                # Lower energy on Mondays, higher on weekends
                base = 6.5 if is_weekend else (5.0 if day_of_week == 0 else 6.0)
                value = base + random.uniform(-2.0, 2.5)
                value = max(float(metric.min_value), min(float(metric.max_value), value))
            elif metric.name_key == "mood":
                # Generally positive with some variation
                value = random.uniform(5.0, 9.0)
            elif metric.name_key == "anxiety_level":
                # Lower anxiety on weekends
                base = 3.5 if is_weekend else 5.0
                value = base + random.uniform(-2.0, 3.0)
                value = max(float(metric.min_value), min(float(metric.max_value), value))
            elif metric.name_key == "stress_level":
                # Similar to anxiety
                base = 3.0 if is_weekend else 5.5
                value = base + random.uniform(-2.0, 3.0)
                value = max(float(metric.min_value), min(float(metric.max_value), value))
            elif metric.name_key == "motivation":
                # Varies more randomly
                value = random.uniform(4.0, 8.5)
            else:
                # Default range value
                min_val = float(metric.min_value)
                max_val = float(metric.max_value)
                value = random.uniform(min_val, max_val)

            return {"value_numeric": Decimal(str(round(value, 2)))}

        elif metric.value_type == "number":
            if metric.name_key == "exercise_minutes":
                # More exercise on weekends
                if is_weekend:
                    value = random.choice([0, 30, 45, 60, 90])
                else:
                    value = random.choice([0, 0, 20, 30, 45])
            elif metric.name_key == "meditation":
                # Occasional meditation
                value = random.choice([0, 0, 0, 5, 10, 15, 20])
            elif metric.name_key == "screen_time":
                # More screen time on weekends
                base = random.uniform(6, 10) if is_weekend else random.uniform(4, 8)
                value = round(base, 1)
            else:
                value = random.randint(0, 100)

            return {"value_numeric": Decimal(str(value))}

        elif metric.value_type == "count":
            if metric.name_key == "water_intake":
                # 4-10 glasses per day
                value = random.randint(4, 10)
            elif metric.name_key == "caffeine_intake":
                # 0-4 cups per day
                value = random.randint(0, 4)
            else:
                value = random.randint(0, 10)

            return {"value_numeric": Decimal(str(value))}

        elif metric.value_type == "boolean":
            if metric.name_key == "headache":
                # 10% chance of headache
                value = random.random() < 0.1
            elif metric.name_key == "social_interaction":
                # More social on weekends
                value = random.random() < (0.8 if is_weekend else 0.5)
            elif metric.name_key in ["morning_medication", "evening_medication"]:
                # 90% adherence
                value = random.random() < 0.9
            elif metric.name_key == "journaling":
                # 30% of days
                value = random.random() < 0.3
            elif metric.name_key == "alcohol":
                # More on weekends
                value = random.random() < (0.4 if is_weekend else 0.1)
            else:
                value = random.random() < 0.5

            return {"value_boolean": value}

        elif metric.value_type == "text":
            return {"value_text": "Sample text entry"}

        return {}

    @classmethod
    def _generate_note(cls, entry_date: date) -> str:
        """Generate a realistic note for an entry."""
        notes = [
            "Had a productive day at work.",
            "Feeling good today, went for a walk in the evening.",
            "Woke up feeling tired but improved as the day went on.",
            "Stressful day with deadlines, need to relax more.",
            "Great day! Spent time with friends.",
            "Feeling a bit anxious, but managed well.",
            "Lazy Sunday, enjoyed relaxing at home.",
            "Busy day but felt accomplished.",
            "Not feeling my best today.",
            "Wonderful day, everything went smoothly.",
            "Felt motivated and got a lot done.",
            "Struggled with focus today.",
            "Had a headache in the afternoon.",
            "Slept really well last night.",
            "Enjoyed my meditation session today.",
            "Missed my workout today, will do better tomorrow.",
            "Feeling grateful for small things today.",
            "A bit overwhelmed with tasks.",
            "Nice weather, spent time outdoors.",
            "Cozy day indoors with a good book."
        ]
        return random.choice(notes)

    @classmethod
    def clear_user_data(cls, db: Session, user: User) -> None:
        """
        Clear all user data (metrics and entries).

        Args:
            db: Database session
            user: User to clear data for
        """
        # Delete all entry values (will cascade from entries)
        db.query(Entry).filter(Entry.user_id == user.id).delete()

        # Delete all metrics (will cascade entry values)
        db.query(Metric).filter(Metric.user_id == user.id).delete()

        db.commit()
