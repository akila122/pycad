from pyautocad import aDouble
from autocad_session import channel


def draw_square(start_x: float = 0, start_y: float = 0, size: float = 100):
    square_cords = aDouble(
        start_x, start_y,
        start_x + size, start_y,
        start_x + size, start_y + size,
        start_x, start_y + size,
    )
    diagonal_cords = aDouble(
        start_x, start_y,
        start_x + size, start_y + size,
    )
    square = channel.session.model.AddLightWeightPolyline(square_cords)
    square.Closed = True
    channel.session.model.AddLightWeightPolyline(diagonal_cords)
