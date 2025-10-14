"""
Create - создание
Read - чтение
Update - обновление
Delete - удаление
"""

import logging

from pydantic import BaseModel, ValidationError

from core.config import MOVIE_CATALOG_STORAGE_FILEPATH

from schemas.movie_url import (
    Movie,
    MovieUpdate,
    MoviePartialUpdate,
)

log = logging.getLogger(__name__)


class MovieStorage(BaseModel):
    slug_to_movie_storage: dict[str, Movie] = {}

    def save_state(self) -> None:
        MOVIE_CATALOG_STORAGE_FILEPATH.write_text(
            self.model_dump_json(indent=2), encoding="utf-8"
        )
        log.info("Saved movie to storage file.")

    @classmethod
    def from_state(cls) -> "MovieStorage":
        if not MOVIE_CATALOG_STORAGE_FILEPATH.exists():
            log.info("movie storage file doesn't exist.")
            return MovieStorage()
        return cls.model_validate_json(
            MOVIE_CATALOG_STORAGE_FILEPATH.read_text(encoding="utf-8")
        )

    def init_storage_from_state(self) -> None:
        try:
            data = MovieStorage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file due to validation error.")
            return

        # мы обновляем свойства напрямую
        # если будут новые свойства
        # то их тоже надо обновить
        self.slug_to_movie_storage.update(
            data.slug_to_movie_storage,
        )
        log.warning("Recovered data from storage file.")

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie_storage.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_movie_storage.get(slug)

    def create(self, movie_create: Movie) -> Movie:
        movie_create = Movie(
            **movie_create.model_dump(),
        )

        self.slug_to_movie_storage[movie_create.slug] = movie_create
        log.info("Create Movie %s", movie_create)
        return movie_create

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie_storage.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        return movie

    def update_partial(
        self,
        movie: Movie,
        movie_in: MoviePartialUpdate,
    ) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        return movie


storage = MovieStorage()

#
# storage = MovieStorage()
#
#
# storage.create(
#     Movie(
#         slug="moscow",
#         title="Москва слезам не верит",
#         year=1979,
#         description="Москва, 1950-е годы. Три молодые провинциалки приезжают в Москву в поисках того,"
#         "что ищут люди во всех столицах мира — любви, счастья и достатка. Антонина выходит замуж,"
#         "растит детей, любит мужа. Людмиле Москва представляется лотереей,"
#         "в которой она должна выиграть свое особенное счастье. Катерина же отчаянно влюбляется,"
#         "но избранник ее оставляет. Однако она не опускает руки, в одиночку растит дочь и к тому же"
#         "успевает делать блестящую карьеру. В 40 лет судьба дарит ей неожиданную встречу.",
#         genre="драма, комедия",
#     )
# )
#
# storage.create(
#     Movie(
#         slug="steel",
#         title="Живая сталь",
#         year=2011,
#         description="События фильма происходят в будущем, где бокс запрещен за негуманностью и заменен боями"
#         "2000-фунтовых роботов, управляемых людьми. Бывший боксер, а теперь промоутер,"
#         "переметнувшийся в Робобокс, решает, что наконец нашел своего чемпиона, когда ему попадается"
#         "выбракованный, но очень способный робот. Одновременно на жизненном пути героя возникает"
#         "11-летний парень, оказывающийся его сыном. И по мере того, как машина пробивает свой путь"
#         "к вершине, обретшие друг друга отец и сын учатся дружить.",
#         genre="научно-фантастическая семейная драма",
#     )
# )
#
# storage.create(
#     Movie(
#         slug="great",
#         title="Великий уравнитель",
#         year=2014,
#         description="Бывший агент ЦРУ, пожилой афроамериканец Роберт Макколл, решил начать жизнь заново,"
#         "оставить непростое прошлое и смотреть в будущее, как и обещал покойной жене. Он уже нашёл обычную"
#         "работу продавца в магазине. Однажды Макколл вступается за юную проститутку Тери,"
#         "с которой болтал в местной закусочной и которая находится под контролем русской мафии."
#         "Макколл прекращает свою добровольную отставку и начинает самостоятельные поиски правосудия. Все,"
#         "кто страдает от криминальных авторитетов, коррумпированных чиновников и не может найти помощи "
#         "у государства, находят помощь в лице Макколла. Он поможет. Потому что он — великий уравнитель.",
#         genre="боевик-триллер",
#     )
# )
