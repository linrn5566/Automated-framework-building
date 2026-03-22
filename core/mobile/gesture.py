from core.logger import log


class MobileGesture:
    def __init__(self, driver):
        self.driver = driver

    def swipe_vertical(self, start_ratio: float = 0.8, end_ratio: float = 0.2, duration: int = 600):
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * start_ratio)
        end_y = int(size['height'] * end_ratio)

        try:
            self.driver.swipe(start_x, start_y, start_x, end_y, duration)
        except AttributeError:
            self.driver.execute_script(
                'mobile: swipeGesture',
                {
                    'left': int(size['width'] * 0.2),
                    'top': int(size['height'] * 0.2),
                    'width': int(size['width'] * 0.6),
                    'height': int(size['height'] * 0.6),
                    'direction': 'up' if end_ratio < start_ratio else 'down',
                    'percent': 0.75,
                },
            )

        log.info(f"执行纵向滑动: {start_ratio} -> {end_ratio}")
