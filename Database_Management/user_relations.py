from neo4j import GraphDatabase

# NOTE - for all statuses, variable 'r' or 'R' must be used for relations, only 1 char. 
class Database:
    """Creates a New Session and sets up Restricted Statements"""

    def __init__(self, uri:str, auth:tuple) -> None:
        """
        Starts the Driver 
        Creates CONSTRAINTS, if not already implemented
        Returns the GraphDatabase.driver object 
        """
        self.uri = uri
        self.auth = auth
        self.driver = GraphDatabase.driver(uri=self.uri, auth=self.auth)
        self.db = self.driver.session()

    def start(self) -> GraphDatabase:
        """

        """

        DATABASE = self.driver.session()

        neo4j_create_statement_1 = "CREATE CONSTRAINT FOR (user:User) REQUIRE user.user_name IS UNIQUE" 
        neo4j_create_statement_2 = "CREATE CONSTRAINT FOR (user:User) REQUIRE user.user_id IS UNIQUE" 
        self.db.run("MATCH (n) DETACH DELETE n")
        try:
            self.db.run(neo4j_create_statement_1)
            self.db.run(neo4j_create_statement_2)
           
        except Exception as e:
            print("Already Exceptions")
            pass
            

    
    def stop(self):
        self.db.close()
    
    def add_user(self, user) -> None:
        #TODO: Improve Drastically, maybe create a new function as well?? 
        created = False 
        testing_idea = []
        while not created:
            statement = "MATCH (user:User) Return (user.user_name)"
            for i in self.db.run(statement):
                name = str(i)[26:-2].lower()
                testing_idea.append(name)
            if user.get_user_name().lower() not in testing_idea:
                neo4j_create_statement = "CREATE (" + user.get_user_name() + ":User {user_name: '" + str(user.get_user_name()) + "'})"
                self.db.run(neo4j_create_statement)
                created = True
            else:
                print("Username not available: " + user.get_user_name())
                break

    def remove_user(self, user) -> None:
        neo4j_create_statement = "MATCH (user:User {user_name: '" + str(user.get_user_name()) + "'})" + "DETACH DELETE user"

        self.db.run(neo4j_create_statement)
    
    def check_status(self, user_name_1:str, user_name_2:str) -> str or None:
        """
        Returns status between two users -> str or None
        args {self, User}
        """
        a = user_name_1
        b = user_name_2

        # MATCH used to search Neo4j DB
        neo4j_create_statement = "MATCH (User {user_name: '" + a + "'})-[r]->(user:User {user_name: '" + b + "'}) Return type(r)"

        status = None
        for i in self.db.run(neo4j_create_statement):
            status = str(i)[17:-2]
            # print(status)
        return status 
    
    def friend_user(self, user_name_1:str, user_name_2:str) -> None: 
        """MATCH user w/ FRIENDS relation"""
        a = user_name_1
        b = user_name_2
        if self.check_status(a, b) == 'BLOCKED':
            question = str(input('This user is BLOCKED. Would you like to UNBLOCK them? (Y/n): ').lower())
            if question == 'y':
                self.unblock_user(a, b)
                neo4j_create_statement = "MATCH (a:User), (b:User)" + "WHERE a.user_name = '" + a + "' AND b.user_name = '" + b + "'"+\
                "CREATE (a)-[r:FRIENDS]->(b)" + "Return a,b"
            else:
                return None
        else:
            neo4j_create_statement = "MATCH (a:User), (b:User)" + "WHERE a.user_name = '" + a + "' AND b.user_name = '" + b + "'"+\
            "CREATE (a)-[r:FRIENDS]->(b)" + "Return a,b"
        self.db.run(neo4j_create_statement)

    def unfriend_user(self, user_name_1:str, user_name_2:str) -> None:
        """
        DELETE FRIENDS relation 
        args {self, User}
        returns None
        """
        a = user_name_1
        b = user_name_2
        neo4j_create_statement = "MATCH (a:User {user_name: '" + a + "'})-[r:FRIENDS]->(b:User {user_name: '" + b + "'})" +\
        "DELETE r"

        self.db.run(neo4j_create_statement)

    def block_user(self, user_name_1:str, user_name_2:str) -> None:
        """MATCH user w/ BLOCKED relation"""
        a = user_name_1
        b = user_name_2
        self.unfollow_user(a, b)
        self.unfriend_user(a, b)
        self.unfollow_user(b, a)
        self.unfriend_user(b, a)

        neo4j_create_statement = "MATCH (a:User), (b:User)" + "WHERE a.user_name = '" + a + "' AND b.user_name = '" + b + "'"+\
        "CREATE (a)-[r:BLOCKED]->(b)" + "Return a,b"

        self.db.run(neo4j_create_statement)

    def unblock_user(self, user_name_1:str, user_name_2:str) -> None:
        """
        DELETE BLOCKED relation 
        args {self, User}
        returns None
        """
        a = user_name_1
        b = user_name_2
        neo4j_create_statement = "MATCH (a:User {user_name: '" + a + "'})-[r:BLOCKED]->(b:User {user_name: '" + b + "'})" +\
        "DELETE r"

        self.db.run(neo4j_create_statement)

    def follow_user(self, user_name_1:str, user_name_2:str) -> None:
        """MATCH user w/ FOLLOWS relation"""
        a = user_name_1
        b = user_name_2

        if self.check_status(a, b) == 'BLOCKED':
            question = str(input('This user is BLOCKED. Would you like to UNBLOCK them? (Y/n): ').lower())
            if question == 'y':
                self.unblock_user(a, b)
                neo4j_create_statement = "MATCH (a:User), (b:User)" + "WHERE a.user_name = '" + a + "' AND b.user_name = '" + b + "'"+\
                "CREATE (a)-[r:FOLLOWS]->(b)" + "Return a,b"
            else:
                return None
        else:
            neo4j_create_statement = "MATCH (a:User), (b:User)" + "WHERE a.user_name = '" + a + "' AND b.user_name = '" + b + "'"+\
            "CREATE (a)-[r:FOLLOWS]->(b)" + "Return a,b"

        self.db.run(neo4j_create_statement)
    
    def unfollow_user(self, user_name_1:str, user_name_2:str) -> None:
        """
        DELETE FOLLOWS relation 
        args {self, User}
        returns None
        """
        a = user_name_1
        b = user_name_2
        neo4j_create_statement = "MATCH (a:User {user_name: '" + a + "'})-[r:FOLLOWS]->(b:User {user_name: '" + b + "'})" +\
        "DELETE r"

        self.db.run(neo4j_create_statement)

class User:
    def __init__(self, user_name:str, user_id:int) -> None:
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
    

    def get_user_name(self) -> str:
        """Returns user_name"""
        return self.user_name
    
    def get_user_id(self) -> int:
        """Returns user_id"""
        return self.user_id

class Image_Post:
    def __init__(self, id, hash, description, creator, upload_time) -> None:
        pass

class Text_Post:
    def __init__(self, id, hash, description, creator, upload_time) -> None:
        pass

class Video_Post:
    def __init__(self, id, hash, description, creator, upload_time) -> None:
        pass
    
    #TODO - What can a Post do? Give data I guess?? 

if __name__ == "__main__":

    new_session = Database(uri="bolt://192.168.0.207:7687", auth=('neo4j', 'adminadmin'))
    new_session.start()

    user_1 = User('a' , 1)
    user_2 = User('b' ,2)
    new_session.add_user(user_1)
    new_session.add_user(user_2)
    new_session.block_user('a', 'b')
    print(new_session.check_status('a','b'))
    new_session.friend_user('b', 'a')
    print(new_session.check_status('a','b'))

    new_session.remove_user(user_1)
    print(new_session.check_status('a','b'))

    new_session.stop()