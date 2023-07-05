from neo4j import GraphDatabase

class User:
    def __init__(self, user_name:str, user_id:int ) -> None:
        """Creates a User type with:
        name 
        id
        """
        self.user_name:str = user_name
        self.user_id:int = user_id
        #TODO - Add more features for a user

    def get_user_name(self) -> str:
        return self.user_name
    
    def get_user_id(self) -> int:
        return self.user_id
    

    def friend_user(self, user, execution_commands:list) -> None: # friend of type User 
        """Creates New Nodes for friends"""
        neo4j_create_statement = "CREATE (a:User {user_name: '" + str(self.get_user_name()) + "' , user_id: " + str(self.get_user_id()) + "})" +\
        "-[:FRIENDED]->(b:User {user_name: '" +  user.get_user_name() + "' , user_id: " + str(user.get_user_id()) + "})"

        execution_commands.append(neo4j_create_statement)

    def block_user(self, user, execution_commands:list) -> None:
        """Creates New Nodes for Blocks"""
        neo4j_create_statement = "CREATE (a:User {user_name: '" + str(self.get_user_name()) + "' , user_id: " + str(self.get_user_id()) + "})" +\
        "-[:BLOCKED]->(b:User {user_name: '" +  user.get_user_name() + "' , user_id: " + str(user.get_user_id()) + "})"

        execution_commands.append(neo4j_create_statement)

    def follow_user(self, user, execution_commands:list) -> None:
        """Creates New Nodes for Followers"""
        neo4j_create_statement = "CREATE (a:User {user_name: '" + str(self.get_user_name()) + "' , user_id: " + str(self.get_user_id()) + "})" +\
        "-[:FOLLOWS]->(b:User {user_name: '" +  user.get_user_name() + "' , user_id: " + str(user.get_user_id()) + "})"

        execution_commands.append(neo4j_create_statement)

transaction_execution_commands:list = ["CREATE CONSTRAINT FOR (user:User) REQUIRE user.user_name IS UNIQUE", "CREATE CONSTRAINT FOR (user:User) REQUIRE user.user_id IS UNIQUE"]

jeff = User("jeff", 456)
mary = User('mary', 300)
steven = User('steven', 460)

jeff.friend_user(mary, transaction_execution_commands)
jeff.block_user(steven, transaction_execution_commands)
# print(transaction_execution_commands)


def execute(execute_commands:list):
    data_base_connection = GraphDatabase.driver(uri="neo4j://localhost:8000", auth=('neo4j', 'password'))
    session = data_base_connection.session()
    for i in execute_commands:
        session.run(i)

execute(transaction_execution_commands)