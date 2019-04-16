import StatSnapFlaskController
from database.SQLStatCommandsDAO import SQLStatCommandsDAO
from database.StatIdDAO import StatIdDAO
if __name__ == "__main__":
    sql_stat_commands_dao = SQLStatCommandsDAO('7742192011')
    StatSnapFlaskController.generate_data(sql_stat_commands_dao)


