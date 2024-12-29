from aiogram import F

has_region = F["middleware_data"]["user"].region.is_not(None)
