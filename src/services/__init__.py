import sqlite3 as sql
from fastapi import HTTPException, status
from math import ceil


def pagination(
    connection: sql.Connection, 
    table: str,
    query: str = " ", 
    itens: list = [],
    page: int = 1,
    rows_per_page: int = 1
    ):

    # Verificaçoes basicas
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="page may not be less than 1")
    
    if rows_per_page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="rows per page may not be less than 1")

    try:
        cursor = connection.execute(f"""
                SELECT COUNT(*)
                FROM {table}
                {query}
            """
        )
    
        itens_count = cursor.fetchone() 
        itens_count = itens_count[0] if itens_count else 0
        pages_count = ceil(itens_count/rows_per_page)

        next = None if pages_count - page < 1 else page + 1
        prev = None if page - 1 < 1 else page - 1

        if not next and prev and page < pages_count:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="page not found")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return {
        "itens": itens,
        "pagination": {
            "pages_count": pages_count,
            "itens_count": itens_count,
            "itens_per_page": rows_per_page,
            "prev": prev,
            "next": next,
            "current": page
        },
        "error": False,
    }

def pagination_like(
        connection: sql.Connection, 
        table: str,
        column: str,
        target: str, 
        itens: list = [],
        page: int = 1,
        rows_per_page: int = 1
    ):

    # Verificaçoes basicas
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="page may not be less than 1")
    
    if rows_per_page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="rows per page may not be less than 1")
    
    try:
        cursor = connection.execute(f"""
                SELECT COUNT()
                FROM {table}
                WHERE {column} LIKE '%{target}%'
            """
        )

        itens_count = cursor.fetchone() 
        itens_count = itens_count[0] if itens_count else 0
        pages_count = ceil(itens_count/rows_per_page)

        next = None if pages_count - page < 1 else page + 1
        prev = None if page - 1 < 1 else page - 1

        if not next and prev and page < pages_count:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="page not found")
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {
        "itens": itens,
        "pagination": {
            "pages_count": pages_count,
            "itens_count": itens_count,
            "itens_per_page": rows_per_page,
            "prev": prev,
            "next": next,
            "current": page
        },
        "error": False,
    }



class SuperService():

    def __init__(self, connection: sql.Connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add(self,
            table: str, 
            item_to_add: dict[str, any]
        ):

        self.cursor.execute(f"""
                INSERT INTO users
                ({item_to_add.keys})
                VALUES
                ({item_to_add.items})
            """
        )
        self.connect.commit()
        
        user = self.find(table=table, query=f"WHERE email = '{item_to_add.get("email")}'")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="new user was not found in bank")
        
        return user[0][0]

    def find(self, 
            table: str, 
            query: str = "WHERE TRUE", 
            page: int = 1,
            rows_per_page: int = 1
        ):

        try:

            cursor = self.connection.execute(f"""
                    SELECT *
                    FROM {table}
                    {query}
                    LIMIT ?
                    OFFSET ?
                """,
                (rows_per_page, rows_per_page*(page-1))
            )
    
            return cursor.fetchall()

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def find_like(self, 
            table: str, 
            column: str,
            target: str, 
            page: int = 1,
            rows_per_page: int = 1
        ):

        try:
            cursor = self.connection.execute(f"""
                    SELECT * 
                    FROM {table}
                    WHERE {column} LIKE '%{target}%'
                    ORDER BY CASE
                        WHEN {column} LIKE '{target}%' THEN 1
                        WHEN {column} LIKE '%{target}%' THEN 2
                        ELSE 3
                    END
                    LIMIT ?
                    OFFSET ?
                """,
                (rows_per_page, rows_per_page*(page-1))
            )
    
            return cursor.fetchall()
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
