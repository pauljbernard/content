#!/usr/bin/env python3
"""
Sales Collateral Engine - Automated Sales Material Generation

Provides automated generation of sales collateral, demo content, ROI calculators,
and competitive positioning materials

Usage:
    from sales_collateral_engine import SalesCollateralEngine

    engine = SalesCollateralEngine()

    # Generate sales deck
    deck = engine.generate_sales_deck(
        product_name="Biology Curriculum 2025",
        target_audience="K-12 School Districts",
        key_features=["Standards-aligned", "Assessment bank", "Digital platform"]
    )

    # Generate ROI calculator
    roi = engine.generate_roi_calculator(
        product_type="curriculum",
        pricing_model="per_student"
    )

    # Generate demo content
    demo = engine.create_demo_package(
        product_line="Mathematics",
        grade_levels=["6", "7", "8"]
    )
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class SalesDeck:
    """Sales presentation deck"""
    deck_id: str
    product_name: str
    target_audience: str
    slides: List[Dict[str, Any]]
    talking_points: Dict[str, List[str]]
    created_at: str


@dataclass
class ROICalculator:
    """ROI calculator for prospects"""
    calculator_id: str
    product_type: str
    cost_factors: List[Dict[str, Any]]
    benefit_factors: List[Dict[str, Any]]
    formulas: Dict[str, str]
    assumptions: Dict[str, Any]


@dataclass
class DemoPackage:
    """Demo content package for prospects"""
    package_id: str
    product_line: str
    demo_items: List[Dict[str, Any]]
    access_instructions: str
    expiration_days: int


class SalesCollateralEngine:
    """Sales collateral and demo content generation"""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize Sales Collateral Engine

        Args:
            data_dir: Directory for sales collateral data
        """
        self.data_dir = data_dir or Path.home() / ".claude" / "agents" / "sales_collateral"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    # ==================== SALES DECK GENERATION ====================

    def generate_sales_deck(
        self,
        product_name: str,
        target_audience: str,
        key_features: List[str],
        pain_points: Optional[List[str]] = None,
        competitive_advantages: Optional[List[str]] = None,
        case_studies: Optional[List[Dict[str, Any]]] = None
    ) -> SalesDeck:
        """
        Generate sales presentation deck

        Args:
            product_name: Product name
            target_audience: Target audience (e.g., "K-12 Districts")
            key_features: List of key product features
            pain_points: Customer pain points addressed
            competitive_advantages: Competitive differentiators
            case_studies: Customer success stories

        Returns:
            SalesDeck object
        """
        deck_id = f"DECK-{int(datetime.utcnow().timestamp())}"

        # Build slide deck
        slides = []

        # Slide 1: Title
        slides.append({
            "slide_number": 1,
            "slide_type": "title",
            "title": product_name,
            "subtitle": f"Transforming Education for {target_audience}",
            "image": "title_image.png"
        })

        # Slide 2: Problem/Pain Points
        if pain_points:
            slides.append({
                "slide_number": 2,
                "slide_type": "problem",
                "title": "The Challenge",
                "content": pain_points,
                "layout": "bullet_list"
            })

        # Slide 3: Solution Overview
        slides.append({
            "slide_number": 3,
            "slide_type": "solution",
            "title": "Our Solution",
            "content": f"{product_name} addresses these challenges with:",
            "features": key_features,
            "layout": "feature_list"
        })

        # Slide 4-N: Key Features (one per feature)
        for i, feature in enumerate(key_features[:5]):  # Max 5 feature slides
            slides.append({
                "slide_number": 4 + i,
                "slide_type": "feature_detail",
                "title": feature,
                "content": f"Deep dive into {feature}",
                "benefits": [
                    "Increases student engagement",
                    "Reduces teacher prep time",
                    "Improves learning outcomes"
                ],
                "demo_screenshot": f"feature_{i+1}_demo.png"
            })

        # Slide: Competitive Advantages
        if competitive_advantages:
            slides.append({
                "slide_number": len(slides) + 1,
                "slide_type": "competitive",
                "title": "Why Choose Us?",
                "content": competitive_advantages,
                "layout": "comparison_table"
            })

        # Slide: Case Studies
        if case_studies:
            for case_study in case_studies[:2]:  # Max 2 case studies
                slides.append({
                    "slide_number": len(slides) + 1,
                    "slide_type": "case_study",
                    "title": f"Success Story: {case_study.get('customer', 'Customer')}",
                    "customer_name": case_study.get('customer', ''),
                    "challenge": case_study.get('challenge', ''),
                    "solution": case_study.get('solution', ''),
                    "results": case_study.get('results', []),
                    "quote": case_study.get('quote', '')
                })

        # Slide: Pricing & Packages
        slides.append({
            "slide_number": len(slides) + 1,
            "slide_type": "pricing",
            "title": "Flexible Pricing Options",
            "packages": [
                {"name": "Starter", "price": "$X per student", "features": ["Core content", "Basic support"]},
                {"name": "Professional", "price": "$Y per student", "features": ["Full content", "Priority support", "Training"]},
                {"name": "Enterprise", "price": "Custom pricing", "features": ["Unlimited access", "Dedicated success manager", "Custom integrations"]}
            ]
        })

        # Slide: Implementation Timeline
        slides.append({
            "slide_number": len(slides) + 1,
            "slide_type": "timeline",
            "title": "Implementation Timeline",
            "phases": [
                {"phase": "Discovery", "duration": "Week 1-2", "activities": ["Needs assessment", "Platform setup"]},
                {"phase": "Onboarding", "duration": "Week 3-4", "activities": ["Teacher training", "Content migration"]},
                {"phase": "Rollout", "duration": "Week 5-6", "activities": ["Pilot classrooms", "Feedback collection"]},
                {"phase": "Full Launch", "duration": "Week 7+", "activities": ["District-wide rollout", "Ongoing support"]}
            ]
        })

        # Slide: Next Steps / CTA
        slides.append({
            "slide_number": len(slides) + 1,
            "slide_type": "cta",
            "title": "Ready to Transform Your Classrooms?",
            "next_steps": [
                "Schedule a personalized demo",
                "Request a pilot program",
                "Get a custom ROI analysis"
            ],
            "contact": {
                "email": "sales@professor.ai",
                "phone": "1-800-PROFESSOR",
                "website": "www.professor.ai/demo"
            }
        })

        # Generate talking points per slide
        talking_points = self._generate_talking_points(slides, product_name, target_audience)

        return SalesDeck(
            deck_id=deck_id,
            product_name=product_name,
            target_audience=target_audience,
            slides=slides,
            talking_points=talking_points,
            created_at=datetime.utcnow().isoformat() + "Z"
        )

    def _generate_talking_points(
        self,
        slides: List[Dict[str, Any]],
        product_name: str,
        target_audience: str
    ) -> Dict[str, List[str]]:
        """Generate talking points for each slide"""
        talking_points = {}

        for slide in slides:
            slide_num = slide["slide_number"]
            slide_type = slide["slide_type"]

            if slide_type == "title":
                talking_points[f"slide_{slide_num}"] = [
                    f"Welcome! Today we'll show how {product_name} transforms education.",
                    f"Designed specifically for {target_audience}",
                    "Let's explore the challenges you face and how we solve them"
                ]
            elif slide_type == "problem":
                talking_points[f"slide_{slide_num}"] = [
                    "These are the top challenges we hear from educators like you",
                    "Each of these pain points has real costs - time, money, and student outcomes",
                    "The good news? We have a solution"
                ]
            elif slide_type == "solution":
                talking_points[f"slide_{slide_num}"] = [
                    f"{product_name} is purpose-built to address these exact challenges",
                    "Let me walk you through our key features",
                    "Each feature directly solves one of the pain points we discussed"
                ]
            elif slide_type == "case_study":
                talking_points[f"slide_{slide_num}"] = [
                    "Here's a real example from a district just like yours",
                    "Notice the measurable results - this is what you can expect",
                    "I'd love to connect you with this customer for a reference call"
                ]
            elif slide_type == "pricing":
                talking_points[f"slide_{slide_num}"] = [
                    "We offer flexible pricing to fit any budget",
                    "Most districts start with Professional and expand from there",
                    "Let's discuss which option makes sense for your needs"
                ]
            elif slide_type == "cta":
                talking_points[f"slide_{slide_num}"] = [
                    "I'd love to schedule a personalized demo for your team",
                    "We can also set up a pilot program at no cost",
                    "What questions can I answer for you today?"
                ]

        return talking_points

    # ==================== ROI CALCULATOR ====================

    def generate_roi_calculator(
        self,
        product_type: str,
        pricing_model: str = "per_student",
        implementation_cost: Optional[float] = None
    ) -> ROICalculator:
        """
        Generate ROI calculator

        Args:
            product_type: Type of product (curriculum, assessment, platform)
            pricing_model: Pricing model (per_student, per_teacher, per_school, enterprise)
            implementation_cost: Optional one-time implementation cost

        Returns:
            ROICalculator object
        """
        calculator_id = f"ROI-{int(datetime.utcnow().timestamp())}"

        # Define cost factors
        cost_factors = [
            {
                "factor": "Software License",
                "description": f"{product_type.title()} platform license",
                "unit": "per student" if pricing_model == "per_student" else "per teacher",
                "typical_cost": 25.0 if pricing_model == "per_student" else 500.0,
                "input_field": "license_cost_per_unit",
                "calculation": "num_units * license_cost_per_unit"
            },
            {
                "factor": "Implementation",
                "description": "One-time setup and training",
                "unit": "one-time",
                "typical_cost": implementation_cost or 10000.0,
                "input_field": "implementation_cost",
                "calculation": "implementation_cost"
            },
            {
                "factor": "Support & Maintenance",
                "description": "Ongoing technical support",
                "unit": "per year",
                "typical_cost": 5000.0,
                "input_field": "annual_support_cost",
                "calculation": "annual_support_cost"
            }
        ]

        # Define benefit factors
        benefit_factors = [
            {
                "benefit": "Teacher Time Savings",
                "description": "Reduced lesson planning and grading time",
                "measurement": "hours per week per teacher",
                "typical_value": 5.0,
                "monetary_value_calculation": "hours_saved * num_teachers * hourly_rate * weeks_per_year",
                "input_fields": ["hours_saved_per_teacher", "num_teachers", "teacher_hourly_rate", "weeks_per_year"]
            },
            {
                "benefit": "Improved Student Outcomes",
                "description": "Increased assessment scores",
                "measurement": "percentage point improvement",
                "typical_value": 8.0,
                "monetary_value_calculation": "score_improvement * value_per_point * num_students",
                "input_fields": ["score_improvement_percentage", "value_per_point", "num_students"],
                "note": "Value per point derived from graduation rates, college readiness, etc."
            },
            {
                "benefit": "Reduced Material Costs",
                "description": "Savings on textbooks and printed materials",
                "measurement": "dollars per student per year",
                "typical_value": 50.0,
                "monetary_value_calculation": "savings_per_student * num_students",
                "input_fields": ["material_savings_per_student", "num_students"]
            },
            {
                "benefit": "Professional Development Savings",
                "description": "Embedded PD reduces external training costs",
                "measurement": "dollars per teacher per year",
                "typical_value": 500.0,
                "monetary_value_calculation": "pd_savings_per_teacher * num_teachers",
                "input_fields": ["pd_savings_per_teacher", "num_teachers"]
            }
        ]

        # ROI formulas
        formulas = {
            "total_costs": "SUM(cost_factors)",
            "total_benefits": "SUM(benefit_factors)",
            "net_benefit": "total_benefits - total_costs",
            "roi_percentage": "(net_benefit / total_costs) * 100",
            "payback_period_months": "(total_costs / (total_benefits / 12))",
            "5_year_value": "(total_benefits * 5) - (total_costs + (annual_costs * 4))"
        }

        # Assumptions
        assumptions = {
            "teacher_hourly_rate": 35.0,
            "weeks_per_year": 40,
            "value_per_point": 100.0,  # Estimated value of 1% score improvement
            "discount_rate": 0.05,  # 5% for NPV calculations
            "inflation_rate": 0.03  # 3% annual inflation
        }

        return ROICalculator(
            calculator_id=calculator_id,
            product_type=product_type,
            cost_factors=cost_factors,
            benefit_factors=benefit_factors,
            formulas=formulas,
            assumptions=assumptions
        )

    def calculate_roi(
        self,
        calculator: ROICalculator,
        inputs: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Calculate ROI with specific inputs

        Args:
            calculator: ROICalculator object
            inputs: Input values for calculation

        Returns:
            ROI calculation results
        """
        # Calculate total costs
        total_costs = 0.0
        cost_breakdown = {}

        for factor in calculator.cost_factors:
            # Simple calculation (in production, use eval() carefully or parse expressions)
            if "license_cost_per_unit" in inputs and "num_units" in inputs:
                cost = inputs.get("license_cost_per_unit", 0) * inputs.get("num_units", 0)
            else:
                cost = factor["typical_cost"]

            cost_breakdown[factor["factor"]] = cost
            total_costs += cost

        # Calculate total benefits
        total_benefits = 0.0
        benefit_breakdown = {}

        for benefit in calculator.benefit_factors:
            # Example calculation for teacher time savings
            if benefit["benefit"] == "Teacher Time Savings":
                hours = inputs.get("hours_saved_per_teacher", benefit["typical_value"])
                num_teachers = inputs.get("num_teachers", 50)
                hourly_rate = inputs.get("teacher_hourly_rate", 35.0)
                weeks = inputs.get("weeks_per_year", 40)

                value = hours * num_teachers * hourly_rate * weeks
            else:
                # Use typical value multiplied by scale
                value = benefit["typical_value"] * inputs.get("num_students", 1000)

            benefit_breakdown[benefit["benefit"]] = value
            total_benefits += value

        # Calculate ROI metrics
        net_benefit = total_benefits - total_costs
        roi_percentage = (net_benefit / total_costs * 100) if total_costs > 0 else 0
        payback_months = (total_costs / (total_benefits / 12)) if total_benefits > 0 else float('inf')
        five_year_value = (total_benefits * 5) - (total_costs + (total_costs * 0.1 * 4))  # Assume 10% annual costs

        return {
            "total_costs": round(total_costs, 2),
            "cost_breakdown": {k: round(v, 2) for k, v in cost_breakdown.items()},
            "total_benefits": round(total_benefits, 2),
            "benefit_breakdown": {k: round(v, 2) for k, v in benefit_breakdown.items()},
            "net_benefit": round(net_benefit, 2),
            "roi_percentage": round(roi_percentage, 1),
            "payback_period_months": round(payback_months, 1) if payback_months != float('inf') else "N/A",
            "five_year_value": round(five_year_value, 2),
            "recommendation": self._generate_roi_recommendation(roi_percentage, payback_months)
        }

    def _generate_roi_recommendation(self, roi_percentage: float, payback_months: float) -> str:
        """Generate ROI recommendation"""
        if roi_percentage > 200 and payback_months < 12:
            return "Excellent ROI - Strong business case for immediate implementation"
        elif roi_percentage > 100 and payback_months < 24:
            return "Good ROI - Favorable business case with acceptable payback period"
        elif roi_percentage > 50:
            return "Moderate ROI - Consider long-term strategic benefits beyond financial metrics"
        else:
            return "Lower ROI - Explore ways to increase benefits or reduce costs"

    # ==================== DEMO PACKAGE CREATION ====================

    def create_demo_package(
        self,
        product_line: str,
        grade_levels: List[str],
        duration_days: int = 30,
        include_assessments: bool = True
    ) -> DemoPackage:
        """
        Create demo content package

        Args:
            product_line: Product line (e.g., "Mathematics", "ELA")
            grade_levels: Grade levels to include
            duration_days: Demo access duration
            include_assessments: Include assessment items

        Returns:
            DemoPackage object
        """
        package_id = f"DEMO-{int(datetime.utcnow().timestamp())}"

        # Build demo content items
        demo_items = []

        for grade in grade_levels:
            # Sample lessons
            demo_items.extend([
                {
                    "item_type": "lesson",
                    "title": f"Grade {grade} {product_line} - Sample Lesson 1",
                    "description": "Interactive lesson with multimedia content",
                    "duration_minutes": 45,
                    "format": "html",
                    "highlights": ["UDL principles", "Interactive activities", "Formative assessments"]
                },
                {
                    "item_type": "lesson",
                    "title": f"Grade {grade} {product_line} - Sample Lesson 2",
                    "description": "Standards-aligned instructional content",
                    "duration_minutes": 45,
                    "format": "html",
                    "highlights": ["Standards alignment", "Differentiation", "Teacher notes"]
                }
            ])

            # Sample assessments
            if include_assessments:
                demo_items.append({
                    "item_type": "assessment",
                    "title": f"Grade {grade} {product_line} - Sample Assessment",
                    "description": "Formative assessment with auto-grading",
                    "num_items": 10,
                    "format": "interactive",
                    "highlights": ["Auto-grading", "Immediate feedback", "Standards reporting"]
                })

        # Add platform tour
        demo_items.append({
            "item_type": "platform_tour",
            "title": "Interactive Platform Tour",
            "description": "Guided tour of all platform features",
            "duration_minutes": 15,
            "format": "interactive",
            "highlights": ["Navigation", "Teacher tools", "Student view", "Reporting"]
        })

        # Access instructions
        access_instructions = f"""
# Demo Access Instructions

Welcome to your {product_line} demo package!

## Accessing Your Demo

1. Visit: https://demo.professor.ai/{package_id}
2. Use demo credentials:
   - Username: demo@yourdomain.com
   - Password: Demo{package_id}

## What's Included

- {len([i for i in demo_items if i['item_type'] == 'lesson'])} sample lessons across grades {', '.join(grade_levels)}
- {len([i for i in demo_items if i['item_type'] == 'assessment'])} sample assessments with auto-grading
- Interactive platform tour
- Full teacher and student views

## Demo Duration

Your demo access expires in {duration_days} days. Contact your sales representative to extend or convert to full access.

## Need Help?

- Email: demo-support@professor.ai
- Phone: 1-800-PROFESSOR
- Live chat: Available in demo platform

## Next Steps

1. Explore the sample content in teacher and student views
2. Try the auto-grading assessment features
3. Review the standards alignment reports
4. Schedule a follow-up call to discuss your needs

Enjoy exploring!
"""

        return DemoPackage(
            package_id=package_id,
            product_line=product_line,
            demo_items=demo_items,
            access_instructions=access_instructions,
            expiration_days=duration_days
        )

    # ==================== COMPETITIVE ANALYSIS ====================

    def generate_competitive_battlecard(
        self,
        competitor_name: str,
        our_product: str
    ) -> Dict[str, Any]:
        """Generate competitive battlecard"""
        return {
            "battlecard_id": f"BATTLE-{int(datetime.utcnow().timestamp())}",
            "competitor": competitor_name,
            "our_product": our_product,
            "sections": {
                "overview": {
                    "competitor_positioning": "How they position themselves",
                    "our_positioning": "Our unique value proposition",
                    "target_customers": "Who uses their product vs. ours"
                },
                "strengths_weaknesses": {
                    "their_strengths": [
                        "Established brand name",
                        "Large customer base"
                    ],
                    "their_weaknesses": [
                        "Legacy technology",
                        "Complex pricing",
                        "Poor customer support"
                    ],
                    "our_advantages": [
                        "Modern cloud-native platform",
                        "Transparent pricing",
                        "Dedicated success managers"
                    ]
                },
                "feature_comparison": {
                    "features": [
                        {
                            "feature": "Standards Alignment",
                            "us": "✅ Automatic alignment to 50+ state standards",
                            "them": "⚠️ Manual alignment required"
                        },
                        {
                            "feature": "Assessment Bank",
                            "us": "✅ 10,000+ items with psychometric validation",
                            "them": "✅ 5,000+ items"
                        },
                        {
                            "feature": "LMS Integration",
                            "us": "✅ One-click integration with all major LMS",
                            "them": "⚠️ Limited to 2-3 platforms"
                        }
                    ]
                },
                "pricing_comparison": {
                    "our_pricing": "$25/student/year",
                    "their_pricing": "$40/student/year",
                    "value_difference": "37% cost savings with better features"
                },
                "win_strategies": [
                    "Emphasize cost savings and ROI",
                    "Demo the modern, intuitive interface",
                    "Offer side-by-side feature comparison",
                    "Provide customer references from competitive wins"
                ],
                "landmines": [
                    "Don't badmouth competitor - focus on our strengths",
                    "If they mention price, talk about total value",
                    "If they're concerned about switching, emphasize migration support"
                ]
            }
        }


if __name__ == "__main__":
    # Example usage
    engine = SalesCollateralEngine()

    # Generate sales deck
    print("=== Sales Deck Generation ===")
    deck = engine.generate_sales_deck(
        product_name="Professor Framework - Biology Curriculum 2025",
        target_audience="K-12 School Districts",
        key_features=[
            "NGSS-Aligned Content",
            "10,000+ Assessment Items",
            "Interactive Simulations",
            "Real-Time Analytics",
            "Teacher Professional Development"
        ],
        pain_points=[
            "Teachers spend 5+ hours/week on lesson planning",
            "Difficulty aligning to state standards",
            "Limited formative assessment tools",
            "Inconsistent curriculum across classrooms"
        ],
        case_studies=[
            {
                "customer": "Springfield USD",
                "challenge": "Low science proficiency scores",
                "solution": "Implemented Professor Framework Biology",
                "results": [
                    "15% increase in assessment scores",
                    "80% teacher adoption rate",
                    "5 hours/week time savings per teacher"
                ],
                "quote": "Professor Framework transformed our science instruction. Teachers love it!"
            }
        ]
    )

    print(f"Deck ID: {deck.deck_id}")
    print(f"Total Slides: {len(deck.slides)}")
    print(f"Talking Points: {len(deck.talking_points)} sections")

    # Generate ROI calculator
    print("\n=== ROI Calculator ===")
    roi_calc = engine.generate_roi_calculator(
        product_type="curriculum",
        pricing_model="per_student",
        implementation_cost=15000.0
    )

    print(f"Calculator ID: {roi_calc.calculator_id}")
    print(f"Cost Factors: {len(roi_calc.cost_factors)}")
    print(f"Benefit Factors: {len(roi_calc.benefit_factors)}")

    # Calculate ROI
    roi_result = engine.calculate_roi(
        roi_calc,
        inputs={
            "license_cost_per_unit": 25.0,
            "num_units": 1000,  # 1000 students
            "num_teachers": 50,
            "hours_saved_per_teacher": 5.0,
            "num_students": 1000
        }
    )

    print(f"\nROI Analysis:")
    print(f"  Total Costs: ${roi_result['total_costs']:,.2f}")
    print(f"  Total Benefits: ${roi_result['total_benefits']:,.2f}")
    print(f"  Net Benefit: ${roi_result['net_benefit']:,.2f}")
    print(f"  ROI: {roi_result['roi_percentage']:.1f}%")
    print(f"  Payback: {roi_result['payback_period_months']} months")
    print(f"  5-Year Value: ${roi_result['five_year_value']:,.2f}")
    print(f"  Recommendation: {roi_result['recommendation']}")

    # Create demo package
    print("\n=== Demo Package ===")
    demo = engine.create_demo_package(
        product_line="Biology",
        grade_levels=["9", "10"],
        duration_days=30,
        include_assessments=True
    )

    print(f"Package ID: {demo.package_id}")
    print(f"Demo Items: {len(demo.demo_items)}")
    print(f"Expiration: {demo.expiration_days} days")

    # Generate competitive battlecard
    print("\n=== Competitive Battlecard ===")
    battlecard = engine.generate_competitive_battlecard(
        competitor_name="Legacy Textbook Co.",
        our_product="Professor Framework"
    )

    print(f"Battlecard ID: {battlecard['battlecard_id']}")
    print(f"Competitor: {battlecard['competitor']}")
    print(f"Win Strategies: {len(battlecard['sections']['win_strategies'])}")
