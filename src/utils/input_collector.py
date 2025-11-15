"""Interactive client input collection"""

from typing import List, Optional
from ..models import Client, Protocol, WeightUnit, Language


class InputCollector:
    """Collect client information interactively"""

    @staticmethod
    def get_valid_input(
        prompt: str,
        validator=None,
        error_message: str = "Invalid input. Please try again.",
        default: Optional[str] = None
    ) -> str:
        """
        Get validated input from user

        Args:
            prompt: Prompt to display
            validator: Function to validate input (returns True if valid)
            error_message: Error message to display on invalid input
            default: Default value if user presses Enter

        Returns:
            Valid user input
        """
        while True:
            if default:
                user_input = input(f"{prompt} (default: {default}): ").strip()
                if not user_input:
                    return default
            else:
                user_input = input(f"{prompt}: ").strip()

            if validator is None or validator(user_input):
                return user_input
            else:
                print(f"❌ {error_message}")

    @staticmethod
    def collect_client_info() -> Client:
        """
        Interactively collect all client information

        Returns:
            Complete Client object
        """
        print("\n" + "="*60)
        print("FITLIFE MEAL PLAN GENERATOR")
        print("="*60 + "\n")

        # Name
        name = InputCollector.get_valid_input(
            "Client Name",
            validator=lambda x: len(x) > 0,
            error_message="Name cannot be empty"
        )

        # Weight
        weight_str = InputCollector.get_valid_input(
            "Body Weight",
            validator=lambda x: x.replace('.', '').isdigit() and float(x) > 0,
            error_message="Weight must be a positive number"
        )
        weight = float(weight_str)

        # Weight unit
        print("\nSelect weight unit:")
        print("1. Pounds (lbs)")
        print("2. Kilograms (kg)")
        unit_choice = InputCollector.get_valid_input(
            "Choice",
            validator=lambda x: x in ['1', '2'],
            error_message="Please enter 1 or 2",
            default="1"
        )
        weight_unit = WeightUnit.LBS if unit_choice == '1' else WeightUnit.KG

        # Body fat percentage
        body_fat_str = InputCollector.get_valid_input(
            "Body Fat Percentage (5-50)",
            validator=lambda x: x.replace('.', '').isdigit() and 5 <= float(x) <= 50,
            error_message="Body fat must be between 5 and 50"
        )
        body_fat_percentage = float(body_fat_str)

        # Protocol
        print("\nSelect Protocol:")
        print("1. SHREDDED (Fat Loss)")
        print("2. MASSIVE (Muscle Gain)")
        protocol_choice = InputCollector.get_valid_input(
            "Choice",
            validator=lambda x: x in ['1', '2'],
            error_message="Please enter 1 or 2"
        )
        protocol = Protocol.SHREDDED if protocol_choice == '1' else Protocol.MASSIVE

        # Height (required for MASSIVE)
        height = None
        if protocol == Protocol.MASSIVE:
            height_str = InputCollector.get_valid_input(
                "Height (inches)",
                validator=lambda x: x.replace('.', '').isdigit() and float(x) > 0,
                error_message="Height must be a positive number"
            )
            height = float(height_str)

        # Training days
        print("\nSelect Training Days (comma-separated):")
        print("Options: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday")
        print("Example: Monday, Wednesday, Friday")

        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        def validate_days(input_str: str) -> bool:
            days = [d.strip() for d in input_str.split(',')]
            return all(day in valid_days for day in days) and len(days) > 0

        training_days_str = InputCollector.get_valid_input(
            "Training Days",
            validator=validate_days,
            error_message=f"Invalid days. Use: {', '.join(valid_days)}"
        )
        training_days = [d.strip() for d in training_days_str.split(',')]

        # HIGH days
        max_high_days = 1 if protocol == Protocol.SHREDDED else 2
        print(f"\nSelect HIGH Calorie Days ({max_high_days} for {protocol.value}):")
        print("These should be training days for maximum benefit")
        print(f"Your training days: {', '.join(training_days)}")

        def validate_high_days(input_str: str) -> bool:
            days = [d.strip() for d in input_str.split(',')]
            return (all(day in valid_days for day in days) and
                    len(days) <= max_high_days and len(days) > 0)

        high_days_str = InputCollector.get_valid_input(
            "HIGH Days",
            validator=validate_high_days,
            error_message=f"Invalid days or too many (max {max_high_days})"
        )
        high_days = [d.strip() for d in high_days_str.split(',')]

        # Language
        print("\nSelect Output Language:")
        print("1. English")
        print("2. Arabic")
        lang_choice = InputCollector.get_valid_input(
            "Choice",
            validator=lambda x: x in ['1', '2'],
            error_message="Please enter 1 or 2",
            default="1"
        )
        language = Language.ENGLISH if lang_choice == '1' else Language.ARABIC

        # Create client object
        client = Client(
            name=name,
            weight=weight,
            weight_unit=weight_unit,
            body_fat_percentage=body_fat_percentage,
            height=height,
            protocol=protocol,
            training_days=training_days,
            high_days=high_days,
            language=language
        )

        # Display summary
        print("\n" + "="*60)
        print("CLIENT PROFILE SUMMARY")
        print("="*60)
        print(f"Name: {client.name}")
        print(f"Weight: {client.weight} {client.weight_unit.value}")
        print(f"Body Fat: {client.body_fat_percentage}%")
        if client.height:
            print(f"Height: {client.height} inches")
        print(f"Protocol: {client.protocol.value}")
        print(f"Training Days: {', '.join(client.training_days)}")
        print(f"HIGH Days: {', '.join(client.high_days)}")
        print(f"Language: {client.language.value}")
        print("="*60 + "\n")

        return client

    @staticmethod
    def confirm_action(prompt: str = "Continue?") -> bool:
        """
        Ask user for yes/no confirmation

        Args:
            prompt: Confirmation prompt

        Returns:
            True if user confirms, False otherwise
        """
        response = InputCollector.get_valid_input(
            f"{prompt} (yes/no)",
            validator=lambda x: x.lower() in ['yes', 'y', 'no', 'n'],
            error_message="Please enter yes or no",
            default="yes"
        )

        return response.lower() in ['yes', 'y']
