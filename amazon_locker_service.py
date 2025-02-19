from abc import ABC, abstractmethod
from enum import Enum

# -------------------------------
# Enumerations for Locker Size and State
# -------------------------------
class LockerSize(Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"

class LockerState(Enum):
    AVAILABLE = "Available"   # Locker is free
    CLOSED = "Closed"         # Locker is assigned (but not yet open)
    OPEN = "Open"             # Locker is open for interaction

# -------------------------------
# Domain Entities: Person, Package, Order
# -------------------------------
class Person:
    def __init__(self, name: str, phone: str):
        self.name = name
        self.phone = phone

class Customer(Person):
    pass

class DeliveryGuy(Person):
    pass

class Package:
    def __init__(self, package_id: str, size: LockerSize):
        self.package_id = package_id
        self.size = size

class Order:
    def __init__(self, order_id: str, customer: Customer, package: Package):
        self.order_id = order_id
        self.customer = customer
        self.package = package
        self.locker = None
        self.otp = None
        self.pickup_deadline = None  # Could be a datetime

# -------------------------------
# Locker and LockerLocation
# -------------------------------
class Locker:
    def __init__(self, locker_id: str, size: LockerSize):
        self.locker_id = locker_id
        self.size = size
        self.state = LockerState.AVAILABLE
        self.assigned_order = None

    def assign_order(self, order: Order):
        if self.state != LockerState.AVAILABLE:
            raise Exception(f"Locker {self.locker_id} is not available")
        self.assigned_order = order
        self.state = LockerState.CLOSED  # Now assigned but not yet open

    def validate_code(self, otp: str) -> bool:
        """
        Validates the provided OTP against the order's OTP.
        """
        if self.assigned_order is None:
            return False
        return self.assigned_order.otp == otp

    def open_with_code(self, otp: str):
        """
        Validates the provided OTP and, if correct, opens the locker.
        """
        if self.state != LockerState.CLOSED:
            raise Exception(f"Locker {self.locker_id} is not in a CLOSED state (current state: {self.state.value})")
        if self.validate_code(otp):
            self.state = LockerState.OPEN
            print(f"Locker {self.locker_id} is now open.")
        else:
            raise Exception("Invalid OTP provided. Cannot open locker.")

    def close(self):
        """
        Closes the locker and releases the assigned order, making it AVAILABLE again.
        """
        if self.state != LockerState.OPEN:
            raise Exception(f"Locker {self.locker_id} cannot be closed (current state: {self.state.value})")
        self.release_order()
        print(f"Locker {self.locker_id} is now closed and available.")

    def release_order(self):
        self.assigned_order = None
        self.state = LockerState.AVAILABLE

class LockerLocation:
    def __init__(self, location_id: str, address: str):
        self.location_id = location_id
        self.address = address
        self.lockers = []  # List of Locker objects

    def add_locker(self, locker: Locker):
        self.lockers.append(locker)

    def find_available_locker(self, size: LockerSize) -> Locker:
        for locker in self.lockers:
            if locker.size == size and locker.state == LockerState.AVAILABLE:
                return locker
        return None

# -------------------------------
# Notification Interface and Implementation
# -------------------------------
class INotifier(ABC):
    @abstractmethod
    def send_otp(self, phone: str, otp: str, message: str):
        pass

    @abstractmethod
    def generate_otp(self) -> str:
        pass

class OTPService(INotifier):
    def send_otp(self, phone: str, otp: str, message: str):
        print(f"Sending OTP {otp} to {phone}: {message}")

    def generate_otp(self) -> str:
        # In a real system, this would generate a random OTP.
        return "123456"

# -------------------------------
# Singleton Implementation Using a Metaclass
# -------------------------------
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

# -------------------------------
# AmazonLockerService: The Central Service (Singleton)
# -------------------------------
class AmazonLockerService(metaclass=SingletonMeta):
    def __init__(self, notifier: INotifier):
        if not hasattr(self, 'initialized'):
            self.notifier = notifier
            self.locker_locations = []  # List of LockerLocation objects
            self.initialized = True

    def add_locker_location(self, location: LockerLocation):
        self.locker_locations.append(location)

    def find_locker_location(self, location_id: str) -> LockerLocation:
        for loc in self.locker_locations:
            if loc.location_id == location_id:
                return loc
        return None

    def assign_locker_for_order(self, order: Order, location_id: str) -> bool:
        location = self.find_locker_location(location_id)
        if not location:
            print(f"Location {location_id} not found")
            return False

        locker = location.find_available_locker(order.package.size)
        if not locker:
            print(f"No available locker of size {order.package.size.value} in location {location_id}")
            return False

        try:
            locker.assign_order(order)
        except Exception as e:
            print(e)
            return False

        order.locker = locker

        otp = self.notifier.generate_otp()
        order.otp = otp
        self.notifier.send_otp(order.customer.phone, otp, "Your locker OTP for package delivery.")
        return True

    def process_return(self, order: Order, location_id: str) -> bool:
        location = self.find_locker_location(location_id)
        if not location:
            print(f"Location {location_id} not found")
            return False

        locker = location.find_available_locker(order.package.size)
        if not locker:
            print(f"No available locker of size {order.package.size.value} in location {location_id}")
            return False

        try:
            locker.assign_order(order)
        except Exception as e:
            print(e)
            return False

        order.locker = locker

        otp = self.notifier.generate_otp()
        order.otp = otp
        self.notifier.send_otp(order.customer.phone, otp, "Your locker OTP for package return.")
        return True

    def pickup_order(self, order: Order, otp: str):
        """
        Process order pickup. The caller must provide the OTP received by the customer.
        """
        locker = order.locker
        if not locker:
            print("Order has no locker assigned")
            return

        try:
            locker.open_with_code(otp)  # Validate the OTP and open the locker
            # Simulate the pickup process here...
            locker.close()  # After pickup, the locker is closed and becomes available again.
        except Exception as e:
            print(e)

# -------------------------------
# Example Usage
# -------------------------------
if __name__ == "__main__":
    # Create the OTP service
    notifier = OTPService()

    # Get the singleton instance of AmazonLockerService
    locker_service = AmazonLockerService(notifier)

    # Create a locker location and add some lockers to it
    location = LockerLocation("LOC1", "123 Main Street")
    location.add_locker(Locker("L1", LockerSize.SMALL))
    location.add_locker(Locker("L2", LockerSize.MEDIUM))
    location.add_locker(Locker("L3", LockerSize.LARGE))
    locker_service.add_locker_location(location)

    # Create a customer and a package
    customer = Customer("Alice", "555-1234")
    package = Package("PKG1", LockerSize.MEDIUM)
    order = Order("ORD1", customer, package)

    # Assign a locker for the order
    print("Assigning locker for order:")
    if locker_service.assign_locker_for_order(order, "LOC1"):
        print(f"Order {order.order_id} assigned to locker {order.locker.locker_id} with state {order.locker.state.value}")

    # Simulate the pickup process (OTP must match the one sent)
    print("Customer attempting to pick up order with OTP:")
    locker_service.pickup_order(order, "123456")
