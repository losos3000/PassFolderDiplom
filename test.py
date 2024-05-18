from sqlalchemy import delete
from server.data.acccess.models import DataUserAccessOrm

query = delete(DataUserAccessOrm).where(DataUserAccessOrm.ds_user_id == 1).where(DataUserAccessOrm.ds_data_id == 2)

print(query)