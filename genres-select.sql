-- ЗАДАНИЕ 2
-- Название и продолжительность самого длительного трека.
SELECT track_name, track_duration FROM Tracks 
WHERE track_duration = (SELECT MAX(track_duration) FROM Tracks);

-- Название треков, продолжительность которых не менее 3,5 минут.
SELECT track_name, track_duration FROM Tracks
WHERE track_duration >= 210;

-- Названия сборников, вышедших в период с 2018 по 2020 год включительно.
SELECT compilation_name FROM Compilations
WHERE compilation_year BETWEEN 2018 AND 2020;

-- Исполнители, чьё имя состоит из одного слова
SELECT performer_name FROM Performers
WHERE performer_name NOT LIKE '% %';

-- Название треков, которые содержат слово «мой» или «my».
SELECT track_name FROM Tracks
WHERE LOWER(track_name) LIKE '%my%' OR LOWER(track_name) LIKE '%мой%';

-- ЗАДАНИЕ 3
-- Количество исполнителей в каждом жанре.
SELECT genre_name, COUNT(performer_id) AS performers_count FROM Genres
LEFT JOIN Genres_Performers gp ON Genres.genre_id = gp.genre_id
GROUP BY Genres.genre_id,  Genres.genre_name;

-- Количество треков, вошедших в альбомы 2019–2020 годов.
SELECT COUNT(track_id) AS track_count FROM Tracks
JOIN Albums ON Albums.album_id = Tracks.album_id 
WHERE Albums.album_year BETWEEN 2019 AND 2020;

-- Средняя продолжительность треков по каждому альбому.
SELECT album_name, AVG(track_duration) AS avg_track_duration FROM Albums 
JOIN Tracks ON Albums.album_id = Tracks.album_id 
GROUP BY Albums.album_id, Albums.album_name;

-- Все исполнители, которые не выпустили альбомы в 2020 году.
SELECT performer_name FROM Performers p
LEFT JOIN Performers_Albums pa ON p.performer_id = pa.performer_id
LEFT JOIN Albums a ON pa.album_id = a.album_id AND a.album_year = 2020
GROUP BY p.performer_id, p.performer_name
HAVING COUNT(a.album_id) = 0;

--Названия сборников, в которых присутствует конкретный исполнитель (выберите его сами).
SELECT DISTINCT c.compilation_name FROM Performers p
JOIN Performers_Albums pa ON p.performer_id = pa.performer_id
JOIN Albums a ON pa.album_id = a.album_id
JOIN Tracks t ON a.album_id = t.album_id
JOIN Tracks_Compilations tc ON t.track_id = tc.track_id
JOIN Compilations c ON tc.compilation_id = c.compilation_id
WHERE p.performer_name= 'Imagine Dragons';


-- ЗАДАНИЕ 4
-- Названия альбомов, в которых присутствуют исполнители более чем одного жанра.
SELECT DISTINCT album_name FROM Albums a
JOIN Performers_Albums pa ON a.album_id = pa.album_id 
JOIN Performers p ON pa.performer_id = p.performer_id
JOIN Genres_Performers gp ON p.performer_id = gp.performer_id
GROUP BY a.album_id, a.album_name, p.performer_id, p.performer_name
HAVING COUNT(gp.genre_id) > 1;

-- Наименования треков, которые не входят в сборники.
SELECT track_name FROM Tracks t
LEFT JOIN Tracks_Compilations tc ON t.track_id = tc.track_id 
WHERE tc.track_id IS NULL;

-- Исполнитель или исполнители, написавшие самый короткий по продолжительности трек, — теоретически таких треков может быть несколько.
SELECT DISTINCT performer_name FROM Performers p
JOIN Performers_Albums pa ON p.performer_id = pa.performer_id 
JOIN Albums a ON pa.album_id = a.album_id 
JOIN Tracks t ON a.album_id = t.album_id
WHERE t.track_duration = (SELECT MIN(track_duration) FROM Tracks);

-- Названия альбомов, содержащих наименьшее количество треков.
SELECT album_name FROM Albums a
LEFT JOIN Tracks t ON a.album_id = t.album_id 
GROUP BY a.album_id, a.album_name
HAVING COUNT(t.track_id) = (
    SELECT MIN(track_count) 
    FROM (
        SELECT COUNT(track_id) AS track_count FROM Tracks
        GROUP BY album_id
    ) AS album_counts
);
