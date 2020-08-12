import random


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class User:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"User({repr(self.name)})"


class SocialGraph:
    def __init__(self):
        self.reset()

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = Queue()

        q.enqueue([starting_vertex])

        visited = set()

        while q.size() > 0:
            path = q.dequeue()
            v = path[-1]

            if v not in visited:
                if v == destination_vertex:
                    return path

                visited.add(v)

                for friend in self.friendships[v]:
                    new_path = list(path)
                    new_path.append(friend)

                    q.enqueue(new_path)

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif (
            friend_id in self.friendships[user_id]
            or user_id in self.friendships[friend_id]
        ):
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def reset(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.reset()
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create friendships
        possible_friendships = []

        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        random.shuffle(possible_friendships)

        for i in range(num_users * avg_friendships // 2):
            friendships = possible_friendships[i]

            self.add_friendship(friendships[0], friendships[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        connections = {}

        for key in self.users:
            visited[key] = False

        q = Queue()

        q.enqueue(user_id)

        while q.size() > 0:
            v = q.dequeue()

            if visited[v] is False:
                path = self.bfs(user_id, v)
                connections[v] = path
                visited[v] = True

                for friend in self.friendships[v]:
                    q.enqueue(friend)

        return connections


if __name__ == "__main__":
    sg = SocialGraph()

    sg.populate_graph(10, 2)

    sg.friendships = {
        1: {8, 10, 5},
        2: {10, 5, 7},
        3: {4},
        4: {9, 3},
        5: {8, 1, 2},
        6: {10},
        7: {2},
        8: {1, 5},
        9: {4},
        10: {1, 2, 6},
    }

    # print(sg.users)
    # print(sg.friendships)
    # sg.get_all_social_paths(1)
    connections = sg.get_all_social_paths(1)
    print(connections)
