class EventSession:
    """Сессия события"""
    def __init__(self, id, time, map_of_seats):
        self.id = id
        self.time = time
        self.map_of_seats = map_of_seats

    def reserve_seat(self, seat_id, user):
        """Бронирование места"""
        self.map_of_seats[seat_id].current_user = user
        self.map_of_seats[seat_id].status = 'забронировано'

    def cancel_reservation(self, seat_id, user):
        """Отвена брони"""
        self.map_of_seats[seat_id].current_user = None
        self.map_of_seats[seat_id].status = 'свободно'

    def purchase_ticket(self, seat_id, user):
        """Оформление покупки"""
        self.map_of_seats[seat_id].current_user = user
        self.map_of_seats[seat_id].status = 'продано'

    def change_seat(self, from_seat_id, to_seat_id, user):
        """Смена места"""
        self.map_of_seats[from_seat_id].current_user = None
        self.map_of_seats[from_seat_id].status = 'свободно'
        self.map_of_seats[to_seat_id].current_user = user
        self.map_of_seats[to_seat_id].status = 'забронировано'


class Seat:
    """Класс места"""
    def __init__(self, id, row, number, status, currentUser):
        self.id = id
        self.row = row
        self.number = number
        self.status = status
        self.currentUser = currentUser


class User:
    """Класс пользователя"""
    def __init__(self, id, name):
        self.id = id
        self.name = name


class BookingCommand:
    """Класс для вывода информации в консоль"""
    def __init__(self):
        ...

    def reserve_seat(self, user, seat_id):
        """Вывод информации по операции Бронирование места"""
        print(user.name, 'reserve seat', seat_id)

    def cancel_reservation(self, user, seat_id):
        """Вывод информации по операции Отвена брони"""
        print(user.name, 'cancel reservation of seat', seat_id)

    def purchase_ticket(self, user, seat_id):
        """Вывод информации по операции Оформление покупки"""
        print(user.name, 'purchase ticket of seat', seat_id)

    def change_seat(self, user, from_seat_id, to_seat_id):
        """Вывод информации по операции Смена места"""
        print(user.name, f'change seat from {from_seat_id} to', to_seat_id)


class BookingProcessor:
    """Класс для проведения процессов операций"""
    def __init__(self, event_session):
        self.event_session = event_session

    def reserve_seat(self, session: EventSession, seatId: int, user: User):
        session.reserve_seat(seatId, user)

    def cancel_reservation(self, session: EventSession,
                           seatId: int, user: User):
        session.cancel_reservation(seatId, user)

    def purchase_ticket(self, session: EventSession, seatId: int, user: User):
        session.purchase_ticket(seatId, user)

    def change_seat(self, session: EventSession, from_seat_id: int,
                    to_seat_id: int, user: User):
        session.change_seat(from_seat_id, to_seat_id, user)


class Operation:
    """Операции для пользователей, чтобы взаимодействовать с сервисом"""
    def __init__(self, booking_processor: BookingProcessor,
                 booking_command: BookingCommand):
        self.booking_processor = booking_processor
        self.booking_command = booking_command

    def execute(self, session: EventSession, seatId: str, user: User):
        ...


class ReserveSeat (Operation):
    """Операция бронирования"""
    def __init__(self, booking_processor: BookingProcessor,
                 booking_command: BookingCommand):
        super().__init__(booking_processor, booking_command)

    def execute(self, session: EventSession, seatId: str, user: User):
        self.booking_processor.reserve_seat(session, seatId, user)
        self.booking_command.reserve_seat(user, seatId)


class CancelReservation (Operation):
    """Отмена бронирования"""
    def __init__(self, booking_processor: BookingProcessor,
                 booking_command: BookingCommand):
        super().__init__(booking_processor, booking_command)

    def execute(self, session: EventSession, seatId: str, user: User):
        self.booking_processor.cancel_reservation(session, seatId, user)
        self.booking_command.cancel_reservation(user, seatId)


class PurchaseTicket (Operation):
    """Подтверждение брони и оплата"""
    def __init__(self, booking_processor: BookingProcessor,
                 booking_command: BookingCommand):
        super().__init__(booking_processor, booking_command)

    def execute(self, session: EventSession, seatId: str, user: User):
        self.booking_processor.purchase_ticket(session, seatId, user)
        self.booking_command.purchase_ticket(user, seatId)


class ChangeSeat (Operation):
    """Операция смиены места брони"""
    def __init__(self, booking_processor: BookingProcessor,
                 booking_command: BookingCommand):
        super().__init__(booking_processor, booking_command)

    def execute(self, session: EventSession, from_seat_id: int,
                to_seat_id: int, user: User):
        self.booking_processor.change_seat(session, from_seat_id,
                                           to_seat_id, user)
        self.booking_command.change_seat(user, from_seat_id, to_seat_id)


user0 = User(0, 'mark')
user1 = User(1, 'vlad')
user2 = User(2, 'georg')

map_of_seats = [Seat(i, i % 4, i + 1, 'свободно', None) for i in range(11)]

event_session = EventSession(0, '20:00', map_of_seats)

booking_command = BookingCommand()
booking_processor = BookingProcessor(event_session)

reserve_seat = ReserveSeat(booking_processor, booking_command)
cancel_reservation = CancelReservation(booking_processor, booking_command)
purchase_ticket = PurchaseTicket(booking_processor, booking_command)
change_seat = ChangeSeat(booking_processor, booking_command)


reserve_seat.execute(event_session, 5, user0)
change_seat.execute(event_session, 5, 6, user0)
cancel_reservation.execute(event_session, 6, user0)
reserve_seat.execute(event_session, 7, user0)
purchase_ticket.execute(event_session, 7, user0)
print('Список мест:', list(map(lambda s: s.status, map_of_seats)))

print()
print("Кажется, не успеваю...")
print("Ну задумка ведь верная, просто не учтено пару условий)")
print("Слишком много времени ушло на осознание, что вообще просят"
      "и на создание базы.")
