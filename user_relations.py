from neo4j import GraphDatabase

# NOTE - for all statuses, variable 'r' or 'R' must be used for relations, only 1 char. 
class Neo4j_Session:
    """Creates a New Session and sets up Restricted Statements"""

    def __init__(self, uri:str, auth:tuple) -> None:
        """
        Creates new GraphDatabase Driver with args {uri, auth}
        Returns None
        Creates CONSTRAINTS, if not already implemented
        """
        self.uri = uri
        self.auth = auth

    def start(self):
        """
        Starts the Driver 
        Creates CONSTRAINTS, if not already implemented
        Returns the GraphDatabase.driver object 
        """
        database_connection = GraphDatabase.driver(uri=self.uri, auth=self.auth)
        # data_base_connection = GraphDatabase.driver(uri="neo4j://localhost:8000", auth=('neo4j', 'password'))
        session = database_connection.session()
        neo4j_create_statement_1 = "CREATE CONSTRAINT FOR (user:User) REQUIRE user.user_name IS UNIQUE" 
        neo4j_create_statement_2 = "CREATE CONSTRAINT FOR (user:User) REQUIRE user.user_id IS UNIQUE" 
        session.run ("MATCH (n) DETACH DELETE n")
        try:
            session.run(neo4j_create_statement_1)
            session.run(neo4j_create_statement_2)
           
        except Exception as e:
            print("Already Exceptions")
            pass

        return session

class User:
    def __init__(self, user_name:str, user_id:int, session ) -> None:
        """
        Creates a User type with:
        name 
        id
        Neo4j session

        Creates a Node in Neo4j with args 
        Returns None
        """

        self.user_name:str = user_name
        self.user_id:int = user_id
        self.session = session 
        
        #TODO: Improve Drastically 
        created = False 
        testing_idea = []
        while not created:
            statement = "MATCH (user:User) Return (user.user_name)"
            for i in self.session.run(statement):
                name = str(i)[26:-2].lower()
                testing_idea.append(name)
            if self.get_user_name().lower() not in testing_idea:
                neo4j_create_statement = "CREATE (" + self.get_user_name() + ":User {user_name: '" + str(self.get_user_name()) +\
                "' , user_id: " + str(self.get_user_id()) + "})"
                self.session.run(neo4j_create_statement)
                created = True
            else:
                print("Username not available")
                break





        
    def get_user_name(self) -> str:
        """Returns user_name"""
        return self.user_name
    
    def get_user_id(self) -> int:
        """Returns user_id"""
        return self.user_id
    
    def check_stats(self, user) -> str or None:
        """
        Returns status between two users -> str or None
        args {self, User}
        """
        a = self.get_user_name()
        b = user.get_user_name()

        # MATCH used to search Neo4j DB
        neo4j_create_statement = "MATCH (User {user_name: '" + a + "'})-[r]->(user:User {user_name: '" + b + "'}) Return type(r)"

        status = None
        for i in self.session.run(neo4j_create_statement):
            status = str(i)[17:-2]
            # print(status)
        return status 
    
    def friend_user(self, user) -> None: 
        """MATCH user w/ FRIENDS relation"""
        a = self.get_user_name()
        b = user.get_user_name()
        neo4j_create_statement = "MATCH (a:User), (b:User)" + "WHERE a.user_name = '" + a + "' AND b.user_name = '" + b + "'"+\
        "CREATE (a)-[r:FRIENDS]->(b)" + "Return a,b"
        self.session.run(neo4j_create_statement)

    def unfriend_user(self, user) -> None:
        """
        DELETE FRIENDS relation 
        args {self, User}
        returns None
        """
        a = self.get_user_name()
        b = user.get_user_name()
        neo4j_create_statement = "MATCH (a:User {user_name: '" + a + "'})-[r:FRIENDS]->(b:User {user_name: '" + b + "'})" +\
        "DELETE r"

        self.session.run(neo4j_create_statement)

    def block_user(self, user) -> None:
        """MATCH user w/ BLOCKED relation"""
        a = self.get_user_name()
        b = user.get_user_name()
        neo4j_create_statement = "MATCH (a:User), (b:User)" + "WHERE a.user_name = '" + a + "' AND b.user_name = '" + b + "'"+\
        "CREATE (a)-[r:BLOCKED]->(b)" + "Return a,b"

        self.session.run(neo4j_create_statement)

    def unblock_user(self, user) -> None:
        """
        DELETE BLOCKED relation 
        args {self, User}
        returns None
        """
        a = self.get_user_name()
        b = user.get_user_name()
        neo4j_create_statement = "MATCH (a:User {user_name: '" + a + "'})-[r:BLOCKED]->(b:User {user_name: '" + b + "'})" +\
        "DELETE r"

        self.session.run(neo4j_create_statement)

    def follow_user(self, user) -> None:
        """MATCH user w/ FOLLOWS relation"""
        a = self.get_user_name()
        b = user.get_user_name()
        neo4j_create_statement = "MATCH (a:User), (b:User) " + " WHERE a.user_name = '" + a + "' AND b.user_name = '" + b + "'"+\
        "CREATE (a)-[r:FOLLOWS]->(b)" + "Return a,b"

        self.session.run(neo4j_create_statement)
    
    def unfollow_user(self, user) -> None:
        """
        DELETE FOLLOWS relation 
        args {self, User}
        returns None
        """
        a = self.get_user_name()
        b = user.get_user_name()
        neo4j_create_statement = "MATCH (a:User {user_name: '" + a + "'})-[r:FOLLOWS]->(b:User {user_name: '" + b + "'})" +\
        "DELETE r"

        self.session.run(neo4j_create_statement)


if __name__ == "__main__":

    new_session = Neo4j_Session(uri="neo4j://localhost:8000", auth=('neo4j', 'password'))
    ses = new_session.start()

    for i in range(50):
        new_user = User(input("Enter a Username: "), i ,ses)


    ses.close()