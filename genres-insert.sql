INSERT INTO Genres(genre_name)
VALUES
('Рок'),
('Поп'),
('Электроника'),
('Хип-хоп'),
('Джаз');

INSERT INTO Performers(performer_name)
VALUES
('Imagine Dragons'),
('Billie Eilish'),
('Daft Punk'),
('Eminem'),
('Adele'),
('The Weeknd'),
('Sting'),
('Beyonce'),
('Radiohead');

INSERT INTO Genres_Performers
VALUES
(1, 1),
(3, 1),
(2, 2),
(3, 2),
(3, 3),
(4, 4),
(1, 4),
(2, 5),
(5, 5),
(2, 6),
(3, 6),
(1, 7),
(5, 7),
(2, 8),
(3, 8),
(1, 9),
(3, 9);

INSERT INTO Albums(album_name, album_year)
VALUES
('Evolve', 2017),
('When We All Fall Asleep', 2019),
('Random Access Memories', 2013),
('The Eminem Show', 2002),
('25', 2015),
('After Hours', 2020),
('The Last Dance', 2019),
('Renaissance', 2020);

INSERT INTO Performers_Albums
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(1, 6),
(7, 7),
(8, 8),
(9, 7);

INSERT INTO Tracks(track_name, track_duration, album_id)
VALUES
('Believer', 204, 1),
('Thunder', 187, 1),
('Bad Guy', 194, 2),
('Ocean Eyes', 196, 2),
('Get Lucky', 368, 3),
('Instant Crush', 335, 3),
('Without Me', 292, 4),
('Lose Yourself', 326, 4),
('Hello', 295, 5),
('When We Were Young', 289, 5),
('Blinding Lights', 200, 6),
('Save Your Tears', 215, 6),
('My Life', 240, 4),
('Мой путь', 210, 5),
('My Way', 225, 6),
('Scarlet', 198, 7),
('Cuff It', 219, 8);

INSERT INTO Compilations(compilation_name, compilation_year)
VALUES
('Лучшие хиты 2010-х', 2020),
('Энергия утра', 2021),
('Романтический вечер', 2022),
('Топ-20 мировых', 2023),
('Лучшее 2018', 2018),
('Хиты 2020', 2020),
('Зимняя коллекция 2019', 2019);

INSERT INTO Tracks_Compilations
VALUES
(1, 1),
(1, 2),
(3, 1),
(3, 2),
(5, 1),
(5, 4),
(7, 1),
(7, 4),
(9, 1),
(9, 3),
(11, 1),
(11, 2),
(11, 4),
(2, 2),
(12, 3),
(4, 3),
(8, 4),
(13, 5),
(14, 6),
(15, 7),
(16, 5),
(17, 6);