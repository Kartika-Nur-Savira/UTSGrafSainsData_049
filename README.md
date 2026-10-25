# UTSGrafSainsData_049

Repository ini berisi pengerjaan Ujian Tengah Semester (UTS) mata kuliah Graf Sains Data menggunakan Neo4j dan Python.

## Deskripsi Proyek

Proyek ini membahas pemodelan dan analisis graf menggunakan Neo4j, serta penerapan graf bipartit untuk merepresentasikan hubungan antara pengunjung (*Visitor*) dan barang (*Item*). Data interaksi digunakan untuk membangun matriks User-Item sebagai dasar analisis kemiripan dan sistem rekomendasi.

## Teknologi yang Digunakan

- Python
- Neo4j
- Cypher Query Language
- Pandas
- NumPy
- SciPy
- NetworkX
- Matplotlib
- Jupyter Notebook

## Implementasi

1. Pemodelan data menggunakan node dan relationship di Neo4j.
2. Pengambilan dan pengelolaan data menggunakan Cypher.
3. Pembentukan graf bipartit User-Item.
4. Pembentukan matriks interaksi User-Item dengan bobot berdasarkan aktivitas pengguna.
5. Analisis karakteristik matriks User-Item dan Item-User.
6. Visualisasi graf menggunakan NetworkX.
7. Pemodelan relasi kemiripan antar-item untuk mendukung sistem rekomendasi.

## Instalasi

Pastikan Python dan Neo4j sudah terpasang. Instal library Python yang diperlukan dengan perintah:

```bash
pip install neo4j pandas numpy scipy networkx matplotlib jupyter
```

## Penggunaan

1. Jalankan Neo4j dan pastikan database dapat diakses.
2. Sesuaikan URI, username, dan password Neo4j pada kode Python.
3. Jalankan query Cypher untuk mengambil data dari database.
4. Jalankan kode Python secara berurutan untuk membentuk matriks, menganalisis graf, dan menampilkan visualisasi.

## Tujuan

Proyek ini bertujuan memahami penerapan teori graf dalam pemodelan relasi data, analisis interaksi pengguna, serta pengembangan sistem rekomendasi berbasis kemiripan item.

## Author

Kartika Nur Savira

