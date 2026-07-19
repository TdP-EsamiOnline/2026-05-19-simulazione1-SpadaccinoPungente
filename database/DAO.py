from database.DB_connect import DBConnect
from model.artist import Artist
from model.genre import Genre


class DAO:
    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select * from genre"""
        cursor.execute(query)
        for row in cursor:
            result.append(Genre(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArtistsByGenre(selected_genre_id):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct ar.ArtistId, ar.Name
                from artist ar
                join album al on ar.ArtistId = al.ArtistId 
                join track tr on al.AlbumId  = tr.AlbumId
                where tr.GenreId = %s
                """
        cursor.execute(query, (selected_genre_id, ))
        for row in cursor:
            result.append(Artist(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArtistsBySharedCostumers(selected_genre_id):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                with CustomerArtists as (
                select distinct i.CustomerId, al.ArtistId
                from invoice i
                join invoiceline il on i.InvoiceId = il.InvoiceId
                join track t on il.TrackId = t.TrackId
                join album al on t.AlbumId = al.AlbumId
                where t.GenreId = %s)
                select distinct t1.ArtistId as a1, t2.ArtistId as a2
                from CustomerArtists t1
                join CustomerArtists t2 on t1.CustomerId = t2.CustomerId
                where t1.ArtistId < t2.ArtistId
                """
        cursor.execute(query, (selected_genre_id, ))
        for row in cursor:
            result.append((row["a1"], row["a2"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPopularities():
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """
                select al.ArtistId, sum(il.Quantity) as popularity
                from invoiceline il
                join track tr on il.TrackId = tr.TrackId
                join album al on tr.AlbumId = al.AlbumId
                group by al.ArtistId
                """
        cursor.execute(query)
        for row in cursor:
            result[row['ArtistId']] = int(row['popularity'])
        cursor.close()
        conn.close()
        return result

