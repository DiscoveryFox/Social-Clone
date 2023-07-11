from neo4j import GraphDatabase
import datetime
import time
import uuid 

class User:
    def __init__(self, user_name:str, email:str, password:str, date_of_birth:time, date_of_joining:time, blocked_status:bool) -> None:
        """
        Creates a User type with:
        user_name
        email
        password
        DOB
        DOJ
        blocked_status

        Returns None
        """

        self.user_name:str = user_name
        self.email:str = email
        self.password:str = password
        self.date_of_birth:int = date_of_birth
        self.date_of_joining:int = date_of_joining
        self.blocked_status:bool = blocked_status
    

    def get_user_name(self) -> str:
        """Returns user_name"""
        return self.user_name
    
    def get_email(self) -> str:
        """Returns email"""
        return self.email

    def get_password(self) -> str:
        """Returns hashed password"""
        return self.password

    def get_date_of_birth(self) -> int:
        """Returns date of birth"""
        return self.date_of_birth

    def get_date_of_joining(self) -> int:
        """Returns date of joining"""
        return self.date_of_joining
    
    def get_blocked_status(self) -> bool:
        """Returns admin given blocked status"""
        return self.blocked_status

class Image_Post:
    def __init__(self, id:uuid, hash:hash, description:str, creator:User, upload_time:time, tags:list) -> None:
        self.id = id
        self.hash = hash
        self.description = description
        self.creator = creator
        self.creator_user_name = creator.get_user_name()
        self.upload_time = upload_time
        self.tags = tags
        pass

class Text_Post:
    def __init__(self, id:uuid, hash:hash, description:str, creator:User, upload_time:time, tags:list) -> None:
        self.id = id
        self.hash = hash
        self.description = description
        self.creator = creator
        self.creator_user_name = creator.get_user_name()
        self.upload_time = upload_time
        self.tags = tags
        pass

class Video_Post:
    def __init__(self, id:uuid, hash:hash, description:str, creator:User, upload_time:time, tags:list) -> None:
        self.id = id
        self.hash = hash
        self.description = description
        self.creator = creator
        self.creator_user_name = creator.get_user_name()
        self.upload_time = upload_time
        self.tags = tags
        pass
    
    #TODO - What can a Post do? Give data I guess?? 

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
                # If user_name is availabe - MUST be UNIQUE 
                neo4j_create_statement = "CREATE (u:User" +\
                "{user_name: '" + str(user.get_user_name()) +"'," +\
                "email: '" + str(user.get_email()) + "'," +\
                "password: '" + str(user.get_password()) + "'," +\
                "data_of_birth: " + str(user.get_date_of_birth()) + "," +\
                "date_of_joining: " + str(user.get_date_of_joining()) + "," +\
                "blocked_status: " + str(user.get_blocked_status()) +\
                "})"

                self.db.run(neo4j_create_statement)
                created = True
            else:
                print("Username not available: " + user.get_user_name())
                break

    def remove_user(self, user:User) -> None:
        neo4j_create_statement = "MATCH (user:User {user_name: '" + str(user.get_user_name()) + "'})" + "DETACH DELETE user"

        self.db.run(neo4j_create_statement)
    
    def check_status(self, user_1:User, user_2:User) -> str or None:
        """
        Returns status between two users -> str or None
        args {self, User}
        """
        a = user_1.get_user_name()
        b = user_2.get_user_name()

        # MATCH used to search Neo4j DB
        neo4j_create_statement = "MATCH (User {user_name: '" + a + "'})-[r]->(user:User {user_name: '" + b + "'}) Return type(r)"

        status = None
        for i in self.db.run(neo4j_create_statement):
            status = str(i)[17:-2]
            # print(status)
        return status 
    
    def friend_user(self, user_1:User, user_2:User) -> None: 
        """MATCH user w/ FRIENDS relation"""
        a = user_1.get_user_name()
        b = user_2.get_user_name()
        if self.check_status(user_1, user_2) == 'BLOCKED':
            question = str(input('This user is BLOCKED. Would you like to UNBLOCK them? (Y/n): ').lower())
            if question == 'y':
                self.unblock_user(a, b)
                self.follow_user(a, b)
                neo4j_create_statement = "MATCH (a:User), (b:User)" + "WHERE a.user_name = '" + a + "' AND b.user_name = '" + b + "'"+\
                "CREATE (a)-[r:FRIENDS]->(b)" + "Return a,b"
            else:
                return None
        elif self.check_status(user_1, user_2) != 'FOLLOWS':
            self.follow_user(user_1, user_2)
            neo4j_create_statement = "MATCH (a:User), (b:User)" + "WHERE a.user_name = '" + a + "' AND b.user_name = '" + b + "'"+\
            "CREATE (a)-[r:FRIENDS]->(b)" + "Return a,b"

        else:
            neo4j_create_statement = "MATCH (a:User), (b:User)" + "WHERE a.user_name = '" + a + "' AND b.user_name = '" + b + "'"+\
            "CREATE (a)-[r:FRIENDS]->(b)" + "Return a,b"
        self.db.run(neo4j_create_statement)

    def unfriend_user(self, user_1:User, user_2:User) -> None:
        """
        DELETE FRIENDS relation 
        args {self, User}
        returns None
        """
        a = user_1.get_user_name()
        b = user_2.get_user_name()
        neo4j_create_statement = "MATCH (a:User {user_name: '" + a + "'})-[r:FRIENDS]->(b:User {user_name: '" + b + "'})" +\
        "DELETE r"

        self.db.run(neo4j_create_statement)

    def block_user(self, user_1:User, user_2:User) -> None:
        """MATCH user w/ BLOCKED relation"""
        a = user_1.get_user_name()
        b = user_2.get_user_name()
        self.unfollow_user(a, b)
        self.unfriend_user(a, b)
        self.unfollow_user(b, a)
        self.unfriend_user(b, a)

        neo4j_create_statement = "MATCH (a:User), (b:User)" + "WHERE a.user_name = '" + a + "' AND b.user_name = '" + b + "'"+\
        "CREATE (a)-[r:BLOCKED]->(b)" + "Return a,b"

        self.db.run(neo4j_create_statement)

    def unblock_user(self, user_1:User, user_2:User) -> None:
        """
        DELETE BLOCKED relation 
        args {self, User}
        returns None
        """
        a = user_1.get_user_name()
        b = user_2.get_user_name()
        neo4j_create_statement = "MATCH (a:User {user_name: '" + a + "'})-[r:BLOCKED]->(b:User {user_name: '" + b + "'})" +\
        "DELETE r"

        self.db.run(neo4j_create_statement)

    def follow_user(self, user_1:User, user_2:User) -> None:
        """MATCH user w/ FOLLOWS relation"""
        a = user_1.get_user_name()
        b = user_2.get_user_name()

        if self.check_status(user_1, user_2) == 'BLOCKED':
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
    
    def unfollow_user(self, user_1:User, user_2:User) -> None:
        """
        DELETE FOLLOWS relation 
        args {self, User}
        returns None
        """
        a = user_1.get_user_name()
        b = user_2.get_user_name()
        neo4j_create_statement = "MATCH (a:User {user_name: '" + a + "'})-[r:FOLLOWS]->(b:User {user_name: '" + b + "'})" +\
        "DELETE r"

        self.db.run(neo4j_create_statement)

if __name__ == "__main__":

    # new_session = Database(uri="bolt://192.168.0.207:7687", auth=('neo4j', 'adminadmin'))
    new_session = Database(uri='neo4j://127.0.0.1:8000', auth=('neo4j', 'password'))
    new_session.start()

    user_1 = User('a' , 'bob.email', "hellow worlds", time.time(), time.time(), False)
    user_2 = User('b' , 'frank.email', "hdsllow worlds", time.time(), time.time(), False)

    new_session.add_user(user_1)
    new_session.add_user(user_2)
    new_session.friend_user(user_1,user_2)


    new_session.stop()