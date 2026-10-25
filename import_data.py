import argparse
import os
import sys

import pandas as pd
from neo4j import GraphDatabase
from tqdm import tqdm


def parse_arguments():
    p = argparse.ArgumentParser(description="Impor dataset RetailRocket ke Neo4j.")
    p.add_argument("-u", "--user", default="neo4j", help="Username Neo4j")
    p.add_argument("-p", "--password", default="eskelapamuda", help="Password Neo4j")
    p.add_argument("-b", "--bolt", default="bolt://127.0.0.1:7687", help="URI Neo4j")
    p.add_argument("-s", "--source", default="data", help="Folder sumber data")
    p.add_argument("-f", "--file", default="item_properties_p1.csv", help="Nama file CSV")
    p.add_argument("-d", "--database", default="neo4j", help="Nama database")
    p.add_argument("--batch", type=int, default=5000, help="Ukuran batch")
    p.add_argument("--reset", action="store_true", help="Hapus semua data lama dulu")
    return p.parse_args()


def create_constraints(session):
    session.run("CREATE CONSTRAINT visitor_id IF NOT EXISTS "
                "FOR (v:Visitor) REQUIRE v.visitorId IS UNIQUE")
    session.run("CREATE CONSTRAINT item_id IF NOT EXISTS "
                "FOR (i:Item) REQUIRE i.itemId IS UNIQUE")


def reset_graph(session, ukuran=5000):
    """Hapus semua simpul dan relasi secara bertahap (aman untuk graf besar)."""
    while True:
        hasil = session.run(
            "MATCH (n) WITH n LIMIT $n DETACH DELETE n RETURN count(*) AS dihapus",
            n=ukuran,
        ).single()
        if hasil["dihapus"] == 0:
            break


CYPHER = """
UNWIND $batch AS row
MERGE (v:Visitor {visitorId: row.visitorid})
MERGE (i:Item {itemId: row.itemid})
FOREACH (_ IN CASE WHEN row.event = 'view' THEN [1] ELSE [] END |
    CREATE (v)-[:VIEWED {timestamp: row.timestamp}]->(i))
FOREACH (_ IN CASE WHEN row.event = 'addtocart' THEN [1] ELSE [] END |
    CREATE (v)-[:ADDED_TO_CART {timestamp: row.timestamp}]->(i))
FOREACH (_ IN CASE WHEN row.event = 'transaction' THEN [1] ELSE [] END |
    CREATE (v)-[:BOUGHT {timestamp: row.timestamp,
                         transactionId: row.transactionid}]->(i))
"""


def import_batch(tx, batch):
    tx.run(CYPHER, batch=batch)


def main():
    args = parse_arguments()

    csv_path = os.path.join(args.source, args.file)
    if not os.path.exists(csv_path):
        print(f"Error: File '{csv_path}' tidak ditemukan!")
        sys.exit(1)

    try:
        driver = GraphDatabase.driver(args.bolt, auth=(args.user, args.password))
        driver.verify_connectivity()
        print("Berhasil terhubung ke Neo4j!")
    except Exception as e:
        print(f"Gagal terhubung ke database: {e}")
        sys.exit(1)

    with driver.session(database=args.database) as session:
        # driver 5.x: execute_write | driver 4.x: write_transaction
        tulis = getattr(session, "execute_write", None) or session.write_transaction

        if args.reset:
            print("Menghapus data lama...")
            reset_graph(session)

        create_constraints(session)

        print(f"Membaca file data dari: {csv_path}")
        with open(csv_path) as f:
            total_rows = sum(1 for _ in f) - 1
        total_chunks = (total_rows // args.batch) + 1
        print(f"Total baris: {total_rows}")

        chunks = pd.read_csv(csv_path, chunksize=args.batch)
        print("Memulai proses impor data ke Neo4j...")
        for chunk in tqdm(chunks, total=total_chunks, desc="Mengimpor Batch Data"):
            # bersihkan transactionid (NaN -> "", 123.0 -> "123")
            tid = pd.to_numeric(chunk["transactionid"], errors="coerce").astype("Int64").astype(str)
            chunk["transactionid"] = tid.replace("<NA>", "")

            tulis(import_batch, chunk.to_dict(orient="records"))

    driver.close()
    print("Proses impor berhasil.")


if __name__ == "__main__":
    main()