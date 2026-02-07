# questions.py
# Form schema: sections -> questions
# Each question:
# - name: stored key in DB
# - label: what the athlete sees
# - type: text, number, date, select, radio, checkbox, textarea, time
# - options: for select/radio/checkbox
# - required: True/False
# - show_if: {"field": "some_name", "equals": "Yes"} or "in": [...]

FORM_SECTIONS = [
    {
        "title": "Start here",
        "description": "This intake helps me build a safe, effective boxing nutrition + weight plan. Please answer as accurately as you can.",
        "questions": [
            {"name": "athlete_name", "label": "Full name (optional)", "type": "text", "required": False},
            {"name": "email", "label": "Email (optional)", "type": "text", "required": False},
            {"name": "consent", "label": "I confirm this information is accurate and I consent to it being used for coaching purposes.", "type": "checkbox_single", "required": True},
        ],
    },

    {
        "title": "1. Athlete Profile & Physiological Background",
        "questions": [
            {"name": "age", "label": "Age", "type": "number", "required": True},
            {"name": "sex", "label": "Sex", "type": "select", "required": True, "options": ["Male", "Female", "Prefer not to say"]},
            {"name": "height", "label": "Height (cm)", "type": "number", "required": True},
            {"name": "current_bodyweight", "label": "Current bodyweight (kg)", "type": "number", "required": True},
            {"name": "bodyweight_measured_date", "label": "Date bodyweight measured", "type": "date", "required": False},
            {"name": "estimated_bodyfat", "label": "Estimated body fat % (if known)", "type": "number", "required": False},

            {"name": "still_growing", "label": "Are you still growing or naturally gaining bodyweight?", "type": "radio", "required": True, "options": ["Yes", "No", "Unsure"]},
            {"name": "grown_height_12m", "label": "Have you grown in height in the last 12 months?", "type": "radio", "required": False, "options": ["Yes", "No", "Unsure"], "show_if": {"field": "still_growing", "in": ["Yes", "Unsure"]}},
            {"name": "natural_weight_gain_12m", "label": "Has your natural bodyweight increased without intentional dieting?", "type": "radio", "required": False, "options": ["Yes", "No", "Unsure"], "show_if": {"field": "still_growing", "in": ["Yes", "Unsure"]}},

            {"name": "competition_weight_class", "label": "Current competition weight class", "type": "text", "required": True},
            {"name": "walk_around_weight", "label": "Walk-around (natural) bodyweight (kg)", "type": "number", "required": True},
            {"name": "offseason_weight_low", "label": "Off-season bodyweight range - low (kg)", "type": "number", "required": False},
            {"name": "offseason_weight_high", "label": "Off-season bodyweight range - high (kg)", "type": "number", "required": False},
            {"name": "lowest_competed_weight", "label": "Lowest bodyweight competed at (kg)", "type": "number", "required": False},
            {"name": "highest_competed_weight", "label": "Highest bodyweight competed at (kg)", "type": "number", "required": False},
            {"name": "time_in_weight_class", "label": "How long have you competed at your current weight class?", "type": "select", "required": False, "options": ["< 6 months", "6–12 months", "1–2 years", "2+ years"]},

            {"name": "bodyweight_12m_ago", "label": "Bodyweight 12 months ago (kg)", "type": "number", "required": False},
            {"name": "largest_weight_loss_for_comp", "label": "Largest weight loss achieved for competition (kg)", "type": "number", "required": False},
            {"name": "fluctuates_over_5pct", "label": "Frequency bodyweight fluctuates >5%", "type": "radio", "required": False, "options": ["Never", "Occasionally", "Frequently"]},
            {"name": "struggle_maintain_between_fights", "label": "Do you struggle to maintain weight between fights?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},
        ],
    },

    {
        "title": "2. Competition Structure & Fight Demands",
        "questions": [
            {"name": "fights_per_year", "label": "Number of fights per year", "type": "number", "required": False},
            {"name": "competition_type", "label": "Type of competitions", "type": "radio", "required": True, "options": ["Single bout events", "Tournaments", "Mixed"]},

            {"name": "tournament_fights", "label": "Typical number of fights per tournament", "type": "number", "required": False, "show_if": {"field": "competition_type", "in": ["Tournaments", "Mixed"]}},
            {"name": "tournament_time_between", "label": "Time between fights", "type": "text", "required": False, "show_if": {"field": "competition_type", "in": ["Tournaments", "Mixed"]}},
            {"name": "tournament_days", "label": "Number of days tournament lasts", "type": "number", "required": False, "show_if": {"field": "competition_type", "in": ["Tournaments", "Mixed"]}},
            {"name": "refuel_between_same_day", "label": "Do you currently refuel between same-day fights?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"], "show_if": {"field": "competition_type", "in": ["Tournaments", "Mixed"]}},
            {"name": "structured_refuel_strategy", "label": "Do you have a structured refueling strategy?", "type": "radio", "required": False, "options": ["Yes", "No"], "show_if": {"field": "competition_type", "in": ["Tournaments", "Mixed"]}},

            {"name": "weighin_timing", "label": "When do weigh-ins usually occur?", "type": "radio", "required": True, "options": ["Same day", "Day before", "Varies"]},
            {"name": "hours_between_weighin_and_fight", "label": "Time between weigh-in and first fight (hours)", "type": "number", "required": False},
            {"name": "multiple_weighins", "label": "Do you weigh in multiple times during tournaments?", "type": "radio", "required": False, "options": ["Yes", "No", "Unsure"]},

            # Performance feedback as frequency (better than yes/no)
            {"name": "dieting_decreases_performance", "label": "Do you notice performance decreases when dieting?", "type": "select", "required": False, "options": ["Never", "Sometimes", "Often", "Always"]},
            {"name": "fade_late_rounds", "label": "Do you fade late in rounds?", "type": "select", "required": False, "options": ["Never", "Sometimes", "Often", "Always"]},
            {"name": "power_decreases_cut", "label": "Do you feel power decreases during weight cuts?", "type": "select", "required": False, "options": ["Never", "Sometimes", "Often", "Always"]},
            {"name": "speed_reaction_decreases_cut", "label": "Do you feel speed/reaction time decreases during cuts?", "type": "select", "required": False, "options": ["Never", "Sometimes", "Often", "Always"]},
            {"name": "durability_decreases_cut", "label": "Do you notice reduced punch resistance/durability when cutting?", "type": "select", "required": False, "options": ["Never", "Sometimes", "Often", "Always"]},
        ],
    },

    {
        "title": "3. Weight Cutting Behaviour & Safety",
        "questions": [
            {"name": "cuts_weight", "label": "Do you cut weight before fights?", "type": "radio", "required": True, "options": ["Yes", "No", "In the past only"]},

            {"name": "typical_cut_amount", "label": "Typical weight cut amount (kg)", "type": "number", "required": False, "show_if": {"field": "cuts_weight", "in": ["Yes", "In the past only"]}},
            {"name": "largest_cut_amount", "label": "Largest weight cut performed (kg)", "type": "number", "required": False, "show_if": {"field": "cuts_weight", "in": ["Yes", "In the past only"]}},
            {"name": "weeks_out_start_dieting", "label": "How many weeks before fights do you begin dieting?", "type": "number", "required": False, "show_if": {"field": "cuts_weight", "in": ["Yes", "In the past only"]}},
            {"name": "cut_weight_split", "label": "How much is typically fat loss vs water loss?", "type": "radio", "required": False, "options": ["Mostly fat loss", "Mixed", "Mostly water loss", "Unsure"], "show_if": {"field": "cuts_weight", "in": ["Yes", "In the past only"]}},

            {"name": "cut_methods", "label": "Methods used (check all that apply)", "type": "checkbox", "required": False,
             "options": [
                 "Food restriction",
                 "Increased cardio volume",
                 "Carb restriction",
                 "Water loading",
                 "Fluid restriction",
                 "Sauna / hot baths",
                 "Sweat suits",
                 "Salt manipulation",
                 "Gut content manipulation (low fibre / low residue dieting)",
                 "Laxatives or diuretics",
                 "Other",
             ],
             "show_if": {"field": "cuts_weight", "in": ["Yes", "In the past only"]}
            },
            {"name": "cut_methods_other", "label": "If other, describe", "type": "text", "required": False,
             "show_if": {"field": "cut_methods", "contains": "Other"}},

            {"name": "cut_symptoms", "label": "Symptoms experienced during cuts (check all that apply)", "type": "checkbox", "required": False,
             "options": [
                 "Missed weight",
                 "Severe fatigue",
                 "Dizziness or fainting",
                 "Muscle cramps",
                 "Reduced training quality",
                 "Mood disturbance",
                 "Sleep disruption",
                 "Reduced motivation",
                 "Injury occurrence during cuts",
             ],
             "show_if": {"field": "cuts_weight", "in": ["Yes", "In the past only"]}
            },

            {"name": "post_weighin_foods", "label": "Typical foods/drinks consumed after weigh-in", "type": "textarea", "required": False,
             "show_if": {"field": "cuts_weight", "in": ["Yes", "In the past only"]}},
            {"name": "post_weighin_refuel_time", "label": "Time taken to refuel after weigh-in", "type": "select", "required": False,
             "options": ["<30 min", "30–60 min", "1–2 hours", "2+ hours", "Varies"],
             "show_if": {"field": "cuts_weight", "in": ["Yes", "In the past only"]}},
            {"name": "weight_regained_pre_fight", "label": "Approximate bodyweight regained before fight (kg)", "type": "number", "required": False,
             "show_if": {"field": "cuts_weight", "in": ["Yes", "In the past only"]}},
            {"name": "fully_recovered_pre_comp", "label": "Do you feel fully recovered before competition?", "type": "radio", "required": False,
             "options": ["Yes", "No", "Sometimes"], "show_if": {"field": "cuts_weight", "in": ["Yes", "In the past only"]}},
        ],
    },

    {
        "title": "4. Training Load & Physical Demands",
        "questions": [
            {"name": "boxing_sessions_per_week", "label": "Boxing sessions per week", "type": "number", "required": False},
            {"name": "avg_session_duration_min", "label": "Average session duration (minutes)", "type": "number", "required": False},

            {"name": "sparring_sessions_per_week", "label": "Sparring sessions per week", "type": "number", "required": False},
            {"name": "sparring_round_duration_min", "label": "Average round duration (minutes)", "type": "number", "required": False},
            {"name": "sparring_total_rounds", "label": "Total rounds per sparring session", "type": "number", "required": False},
            {"name": "sparring_intensity", "label": "Typical sparring intensity", "type": "radio", "required": False, "options": ["Light", "Moderate", "Hard", "Mixed"]},

            {"name": "structured_strength_program", "label": "Do you follow a structured strength program?", "type": "radio", "required": False, "options": ["Yes", "No"]},
            {"name": "strength_sessions_per_week", "label": "Strength sessions per week", "type": "number", "required": False},
            {"name": "conditioning_sessions_per_week", "label": "Conditioning sessions per week", "type": "number", "required": False},
            {"name": "roadwork_frequency", "label": "Running / roadwork frequency (sessions per week)", "type": "number", "required": False},
            {"name": "weekly_training_hours", "label": "Estimated weekly training hours total", "type": "number", "required": False},

            {"name": "training_times", "label": "Usual training times", "type": "checkbox", "required": False, "options": ["Morning", "Afternoon", "Evening", "Multiple daily sessions"]},
            {"name": "two_a_days", "label": "Do you regularly perform two-a-day sessions?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},

            {"name": "camp_volume_increase", "label": "Does training volume increase during camps?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},
            {"name": "camp_sparring_increase", "label": "Does sparring frequency increase during camps?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},
            {"name": "camp_intensity_increase", "label": "Does intensity increase during camps?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},
            {"name": "camp_recovery_decrease", "label": "Does recovery decrease during camps?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},
        ],
    },

    {
        "title": "5. Recovery, Fatigue & Monitoring",
        "questions": [
            {"name": "sleep_hours", "label": "Average nightly sleep duration (hours)", "type": "number", "required": False},
            {"name": "sleep_quality", "label": "Sleep quality", "type": "radio", "required": False, "options": ["Poor", "Average", "Good"]},
            {"name": "bedtime", "label": "Bedtime", "type": "time", "required": False},
            {"name": "wake_time", "label": "Wake time", "type": "time", "required": False},
            {"name": "sleep_disruptions_camp", "label": "Sleep disruptions during camps?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},

            {"name": "recover_between_sessions", "label": "Do you recover well between sessions?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},
            {"name": "constantly_fatigued_camp", "label": "Do you feel constantly fatigued during camps?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},
            {"name": "persistent_soreness", "label": "Do you experience persistent muscle soreness?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},
            {"name": "reduced_motivation_camp", "label": "Do you experience reduced motivation during camps?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},

            {"name": "track_rhr", "label": "Do you track resting heart rate?", "type": "radio", "required": False, "options": ["Yes", "No"]},
            {"name": "track_hrv", "label": "Do you track HRV or recovery metrics?", "type": "radio", "required": False, "options": ["Yes", "No"]},
            {"name": "track_bodyweight", "label": "Do you track bodyweight regularly?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},

            {"name": "current_injuries", "label": "Current injuries", "type": "textarea", "required": False},
            {"name": "previous_injuries", "label": "Previous injuries affecting performance", "type": "textarea", "required": False},
            {"name": "injuries_during_cuts", "label": "Injuries that occur during weight cuts or camps", "type": "textarea", "required": False},
        ],
    },

    {
        "title": "6. Current Eating Behaviour",
        "questions": [
            {"name": "typical_training_day_intake", "label": "Typical training day intake (meals, snacks, drinks, supplements)", "type": "textarea", "required": False},
            {"name": "typical_rest_day_intake", "label": "Typical rest day intake (meals, snacks, drinks, supplements)", "type": "textarea", "required": False},

            {"name": "meals_per_day", "label": "Meals per day", "type": "number", "required": False},
            {"name": "snack_frequency", "label": "Snack frequency (per day)", "type": "number", "required": False},
            {"name": "meal_timing_changes", "label": "Do meal timings change around training?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},

            {"name": "pre_training_food", "label": "What do you eat before training?", "type": "textarea", "required": False},
            {"name": "pre_training_timing", "label": "How long before training do you eat?", "type": "text", "required": False},
            {"name": "train_fasted", "label": "Do you ever train fasted?", "type": "radio", "required": False, "options": ["Never", "Sometimes", "Often"]},
            {"name": "food_pre_training_effect", "label": "Does food before training improve or worsen performance?", "type": "select", "required": False, "options": ["Improves", "Worsens", "No difference", "Unsure"]},

            {"name": "eat_after_training", "label": "Do you eat after training?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},
            {"name": "post_training_delay", "label": "Time delay before post-training meal", "type": "select", "required": False, "options": ["<30 min", "30–60 min", "1–2 hours", "2+ hours", "Varies"]},
            {"name": "post_training_foods", "label": "Typical post-training foods", "type": "textarea", "required": False},

            {"name": "eat_after_late_sessions", "label": "Do you eat after late sessions?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},
            {"name": "struggle_eat_after_hard_training", "label": "Do you struggle to eat after hard training?", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},
        ],
    },

    {
        "title": "7. Appetite & Energy Regulation",
        "questions": [
            {"name": "appetite_highest", "label": "When appetite is highest", "type": "radio", "required": False, "options": ["Morning", "Afternoon", "Evening"]},
            {"name": "struggle_eat_enough", "label": "Do you struggle to eat enough?", "type": "radio", "required": False, "options": ["Never", "Sometimes", "Often"]},
            {"name": "lose_appetite_heavy_training", "label": "Do you lose appetite during heavy training?", "type": "radio", "required": False, "options": ["Never", "Sometimes", "Often"]},
            {"name": "energy_crashes_training", "label": "Do you experience energy crashes during training?", "type": "radio", "required": False, "options": ["Never", "Sometimes", "Often"]},
            {"name": "lowest_daily_energy", "label": "When do you feel lowest daily energy?", "type": "radio", "required": False, "options": ["Morning", "Afternoon", "Evening"]},
            {"name": "hunger_changes_camp", "label": "Do hunger levels change during fight camps?", "type": "select", "required": False, "options": ["Higher", "Lower", "No change", "Unsure"]},
        ],
    },

    {
        "title": "8. Hydration & Electrolyte Behaviour",
        "questions": [
            {"name": "daily_fluid_intake", "label": "Estimated daily fluid intake (litres)", "type": "number", "required": False},
            {"name": "heavy_sweater", "label": "Do you sweat heavily?", "type": "radio", "required": False, "options": ["Yes", "No", "Unsure"]},
            {"name": "visible_salt_loss", "label": "Do you get visible salt loss on clothing/skin?", "type": "radio", "required": False, "options": ["Yes", "No", "Unsure"]},
            {"name": "muscle_cramps", "label": "Do you experience muscle cramps?", "type": "radio", "required": False, "options": ["Never", "Sometimes", "Often"]},
            {"name": "monitor_urine_colour", "label": "Do you monitor urine colour?", "type": "radio", "required": False, "options": ["Yes", "No"]},
            {"name": "electrolyte_drinks", "label": "Do you use electrolyte drinks?", "type": "radio", "required": False, "options": ["Never", "Sometimes", "Often"]},
            {"name": "restrict_fluids_pre_weighin", "label": "Do you deliberately restrict fluids before weigh-ins?", "type": "radio", "required": False, "options": ["Yes", "No"]},
        ],
    },

    {
        "title": "9. Food Preferences & Practical Constraints",
        "questions": [
            {"name": "favourite_foods", "label": "Favourite foods (home cooked & takeaway)", "type": "textarea", "required": False},
            {"name": "disliked_foods", "label": "Foods disliked", "type": "textarea", "required": False},
            {"name": "ethical_religious_restrictions", "label": "Foods refused for ethical/religious reasons", "type": "textarea", "required": False},

            {"name": "cooking_ability", "label": "Cooking ability", "type": "radio", "required": False, "options": ["Poor", "Basic", "Good"]},
            {"name": "meal_prep_time", "label": "Time available for meal prep", "type": "select", "required": False, "options": ["Very low", "Low", "Moderate", "High"]},
            {"name": "fridge_access", "label": "Access to fridge during day", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},
            {"name": "food_between_sessions", "label": "Access to food between sessions", "type": "radio", "required": False, "options": ["Yes", "No", "Sometimes"]},

            {"name": "grocery_limitations", "label": "Grocery access limitations", "type": "textarea", "required": False},
            {"name": "budget_concerns", "label": "Weekly food budget concerns", "type": "radio", "required": False, "options": ["None", "Some", "Major"]},

            {"name": "family_meal_structure", "label": "Family meal structure", "type": "textarea", "required": False},
            {"name": "cultural_food_traditions", "label": "Cultural food traditions", "type": "textarea", "required": False},
            {"name": "takeaway_frequency", "label": "Frequency of eating out/takeaway", "type": "select", "required": False, "options": ["Never", "1–2x/week", "3–5x/week", "Daily"]},
        ],
    },

    {
        "title": "10. Psychological & Behavioural Factors",
        "questions": [
            {"name": "pressure_stay_lean", "label": "Do you feel pressure to stay lean year-round?", "type": "select", "required": False, "options": ["Never", "Sometimes", "Often", "Always"]},
            {"name": "scale_affects_mood", "label": "Does scale weight affect mood?", "type": "select", "required": False, "options": ["Never", "Sometimes", "Often", "Always"]},
            {"name": "weighin_anxiety", "label": "Do weigh-ins cause anxiety?", "type": "select", "required": False, "options": ["Never", "Sometimes", "Often", "Always"]},

            {"name": "emotional_eating_triggers", "label": "Emotional eating triggers", "type": "textarea", "required": False},
            {"name": "stress_eating", "label": "Stress eating behaviour", "type": "textarea", "required": False},
            {"name": "boredom_eating", "label": "Boredom eating behaviour", "type": "textarea", "required": False},
            {"name": "binge_restrict_history", "label": "History of binge/restrict cycles", "type": "radio", "required": False, "options": ["Yes", "No", "Prefer not to say"]},
            {"name": "extreme_dieting_history", "label": "History of extreme dieting?", "type": "radio", "required": False, "options": ["Yes", "No", "Prefer not to say"]},

            {"name": "dieting_style_preference", "label": "Preferred approach", "type": "checkbox", "required": False,
             "options": ["Structured meal plans", "Flexible calorie targets", "Food tracking", "Portion-based guidance"]},
            {"name": "meal_variety_preference", "label": "Meal variety preference", "type": "radio", "required": False, "options": ["Repetitive meals", "Variety"]},
        ],
    },

    {
        "title": "11. Medical & Health Screening",
        "questions": [
            {"name": "medical_conditions", "label": "Medical conditions", "type": "textarea", "required": False},
            {"name": "hormonal_disorders", "label": "Hormonal/endocrine disorders", "type": "textarea", "required": False},
            {"name": "digestive_issues", "label": "Digestive issues", "type": "textarea", "required": False},
            {"name": "allergies_intolerances", "label": "Food allergies or intolerances", "type": "textarea", "required": False},
            {"name": "current_medications", "label": "Current medications", "type": "textarea", "required": False},
            {"name": "current_supplements", "label": "Current supplements", "type": "textarea", "required": False},

            {"name": "history_flags", "label": "History of (check all that apply)", "type": "checkbox", "required": False,
             "options": ["Iron deficiency", "Vitamin D deficiency", "RED-S symptoms", "Stress fractures"]},

            {"name": "menstrual_cycle_regular", "label": "Menstrual cycle regularity (if applicable)", "type": "text", "required": False,
             "show_if": {"field": "sex", "equals": "Female"}},
            {"name": "menstrual_changes_dieting", "label": "Changes during dieting or heavy training (if applicable)", "type": "textarea", "required": False,
             "show_if": {"field": "sex", "equals": "Female"}},
        ],
    },

    {
        "title": "12. Lifestyle & Schedule Constraints",
        "questions": [
            {"name": "work_school_schedule", "label": "School/work schedule", "type": "textarea", "required": False},
            {"name": "shift_work", "label": "Shift work or irregular hours", "type": "textarea", "required": False},
            {"name": "travel_time_gym", "label": "Travel time to gym", "type": "text", "required": False},
            {"name": "ability_eat_at_work", "label": "Ability to eat during school/work", "type": "radio", "required": False, "options": ["Easy", "Some limitations", "Very difficult"]},
            {"name": "routine_stability", "label": "Daily routine stability", "type": "radio", "required": False, "options": ["Consistent", "Variable"]},
        ],
    },

    {
        "title": "13. Nutrition & Diet History",
        "questions": [
            {"name": "tracked_before", "label": "Have you tracked calories/macros before?", "type": "radio", "required": False, "options": ["Yes", "No"]},
            {"name": "previous_calories", "label": "Approximate calories previously consumed", "type": "text", "required": False},
            {"name": "weight_change_at_previous_intake", "label": "Did bodyweight change at that intake?", "type": "text", "required": False},
            {"name": "diets_attempted", "label": "Diets previously attempted", "type": "textarea", "required": False},
            {"name": "what_worked", "label": "What worked well?", "type": "textarea", "required": False},
            {"name": "what_failed", "label": "What failed?", "type": "textarea", "required": False},
            {"name": "previous_coaching", "label": "Previous nutrition coaching experience?", "type": "radio", "required": False, "options": ["Yes", "No"]},
        ],
    },

    {
        "title": "14. Performance & Body Composition Goals",
        "questions": [
            {"name": "primary_goals", "label": "Primary goals (check all that apply)", "type": "checkbox", "required": False,
             "options": [
                 "Make weight safely",
                 "Improve endurance",
                 "Improve power",
                 "Improve recovery",
                 "Improve body composition",
                 "Improve training energy",
                 "Improve tournament performance",
             ]},

            {"name": "next_fight_date", "label": "Next fight date", "type": "date", "required": False},
            {"name": "fights_this_season", "label": "Expected number of fights this season", "type": "number", "required": False},
            {"name": "long_term_goals", "label": "Long-term boxing goals", "type": "textarea", "required": False},
            {"name": "target_body_comp_goal", "label": "Target bodyweight or body composition goal", "type": "textarea", "required": False},
        ],
    },

    {
        "title": "15. Monitoring & Communication Preferences",
        "questions": [
            {"name": "checkin_frequency", "label": "Preferred check-in frequency", "type": "select", "required": False,
             "options": ["Weekly", "Every 2 weeks", "Monthly", "As needed"]},
            {"name": "preferred_metrics", "label": "Preferred progress metrics", "type": "checkbox", "required": False,
             "options": ["Scale weight", "Training performance", "Physique changes", "Energy levels", "Recovery", "Sparring quality"]},

            {"name": "comfort_tools", "label": "Comfort with monitoring tools", "type": "checkbox", "required": False,
             "options": ["Daily weigh-ins", "Food logging", "Progress photos", "Performance testing"]},
        ],
    },
]


def flatten_questions(sections: list[dict]) -> list[dict]:
    flat: list[dict] = []
    for section in sections:
        for q in section.get("questions", []):
            # athlete_name + email live in Start here, but we skip them in POST parsing in app.py
            if q["name"] in ("athlete_name", "email"):
                continue
            flat.append(q)
    return flat

