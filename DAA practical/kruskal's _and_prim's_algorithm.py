import heapq


# ---------------- Union-Find (Disjoint Set) ----------------
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        # Path Compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False

        # Union by Rank
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1

        return True


# ---------------- Kruskal Algorithm ----------------
def kruskal(n, edges):
    """
    n     : Number of vertices
    edges : List of (weight, u, v)
    """

    edges = sorted(edges)

    mst = []
    total_cost = 0

    uf = UnionFind(n)

    for weight, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, weight))
            total_cost += weight

            if len(mst) == n - 1:
                break

    if len(mst) != n - 1:
        print("Warning: Graph is disconnected. MST cannot be formed.")

    return mst, total_cost


# ---------------- Prim Algorithm ----------------
def prim(n, adj, start=0):
    """
    n     : Number of vertices
    adj   : Adjacency List
    start : Starting vertex
    """

    key = [float("inf")] * n
    parent = [-1] * n
    visited = [False] * n

    key[start] = 0

    pq = [(0, start)]

    mst = []
    total_cost = 0

    while pq:
        _, u = heapq.heappop(pq)

        if visited[u]:
            continue

        visited[u] = True

        if parent[u] != -1:
            mst.append((parent[u], u, key[u]))
            total_cost += key[u]

        for v, weight in adj.get(u, []):
            if not visited[v] and weight < key[v]:
                key[v] = weight
                parent[v] = u
                heapq.heappush(pq, (weight, v))

    if len(mst) != n - 1:
        print("Warning: Graph is disconnected. MST cannot be formed.")

    return mst, total_cost


# ---------------- Main Program ----------------
def main():
    n = 7

    edges = [
        (7, 0, 1),
        (5, 0, 3),
        (8, 1, 2),
        (9, 1, 3),
        (7, 1, 4),
        (5, 2, 4),
        (15, 3, 4),
        (6, 3, 5),
        (8, 4, 5),
        (9, 4, 6),
        (11, 5, 6),
    ]

    # Build Adjacency List
    adj = {}

    for weight, u, v in edges:
        adj.setdefault(u, []).append((v, weight))
        adj.setdefault(v, []).append((u, weight))

    # Run Kruskal
    kruskal_mst, kruskal_cost = kruskal(n, edges)

    # Run Prim
    prim_mst, prim_cost = prim(n, adj)

    # Display Results
    print("=" * 35)
    print("Kruskal's Minimum Spanning Tree")
    print("=" * 35)

    for u, v, w in kruskal_mst:
        print(f"{u} -- {v}   Weight = {w}")

    print(f"\nTotal MST Cost = {kruskal_cost}")

    print("\n" + "=" * 35)
    print("Prim's Minimum Spanning Tree")
    print("=" * 35)

    for u, v, w in prim_mst:
        print(f"{u} -- {v}   Weight = {w}")

    print(f"\nTotal MST Cost = {prim_cost}")

    if kruskal_cost == prim_cost:
        print("\n✓ Both algorithms produced the same MST cost.")
    else:
        print("\n✗ MST costs are different.")


if __name__ == "__main__":
    main()
