from fastapi import HTTPException, status
from sqlalchemy import Select, select, func
from src import Model, db, session_db
from typing import Any

class SuperService():
    def get_all_with_pagination(
        self,
        statement: Select,
        page: int = 1,
        rows_per_page: int = 10
    ):
        offset = (page - 1) * rows_per_page
        limit = rows_per_page if rows_per_page >= 0 else 10 
        # Devido ao limit negativo pegar todos os arquivos do banco e isso pode quebrar tudo
       
        try:
            stmt_with_pagination = statement.offset(offset).limit(limit)
            record_list = session_db.execute(stmt_with_pagination).scalars().all()
            
            coumt_stmt = select(func.count()).select_from(statement.subquery()) 
            total = session_db.execute(coumt_stmt).scalar()
       
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Databank error.\n{e}")

        return record_list, total

    def get_all_without_pagination(
        self,
        statement: Select,
    ):
        try:
            record_list = session_db.execute(statement).scalars().all()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Databank error.\n{e}")

        return record_list

    def get(
            self,
            statement: Select
    ):
        try:
            record = session_db.execute(statement).scalar_one_or_none()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Databank error.\n{e}")

        return record 

    def get_by_id(
            self,
            record_id: int, 
            record_class: type[Model]
    ) -> Any | None:
        try:
            stmt = select(record_class).filter_by(id=record_id)
            record = session_db.execute(stmt).scalar_one_or_none()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Databank error.\n{e}")

        return record
    
    def add(
            self,
            record
        ):
        try:
            session_db.add(record)
            session_db.commit()
        except Exception as e:
            session_db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Databank error.\n{e}")

        return record

    def edit(
            self,
            statement: Select,
            fields
        ):
        record = self.get(statement)
        
        if record is None:
            return None
        
        try:
            updated_fields: dict = fields.model_dump(exclude_unset=True)

            for field, value in updated_fields.items():
                if value is not None:
                    setattr(record, field, value)

            session_db.commit()
        except Exception as e:
            session_db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Databank error.\n{e}")

        return record
    
    def edit_by_id(
            self,
            record_id: int,
            record_class: type[Model],
            fields
        ):
        record = self.get_by_id(record_id, record_class)
        
        if record is None:
            return None
        
        try:
            updated_fields: dict = fields.model_dump(exclude_unset=True)

            for field, value in updated_fields.items():
                if value is not None:
                    setattr(record, field, value)

            session_db.commit()
        except Exception as e:
            session_db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Databank error.\n{e}")

        return record
    
    def delete(
            self,
            statement: Select
        ):
        record = self.get(statement)
        
        if record is None:
            return None

        try:
            session_db.delete(record)
            session_db.commit()
        except Exception as e:
            session_db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Databank error.\n{e}")

        return record
    
    def delete_by_id(
            self,
            record_id: int,
            record_class: type[Model]
        ):
        record = self.get_by_id(record_id, record_class)
        
        if record is None:
            return None

        try:
            session_db.delete(record)
            session_db.commit()
        except Exception as e:
            session_db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Databank error.\n{e}")

        return record
