<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quản lý thuốc</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.3.0/css/all.min.css" integrity="sha512-SzlrxWUlpfuzQ+pcUCosxcglQRNAq/DZjVsC0lE40xsADsfeQoEypE+enwcOiGjk/bSuGGKHEyjSoQ1zVisanQ==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="css/style_login.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }

        .container {
            width: 100%;
            max-width: 1200px;
            margin: 20px auto;
            padding: 20px;
            background-color: #c7dcff;
            border-radius: 8px;
        }


        .form {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            background-color: #96b5d7;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        .form label {
            width: 100%;
            font-weight: bold;
        }

        .form input[type="text"],
        .form input[type="date"] {
            width: 100%;
            padding: 8px;
            border: none;
            border-radius: 5px;
            background-color: #eef7ff;
        }

        .form-group {
            flex: 1 1 calc(33.333% - 10px);
        }

        .form-icons {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-left: auto;
        }

        .form-icons .btn {
            background-color: #4a90e2;
            color: white;
            border-radius: 5px;
            padding: 8px 12px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .form-icons .btn .bi {
            font-size: 20px;
        }

        .table-container {
            background-color: #96b5d7;
            padding: 20px;
            border-radius: 8px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        th, td {
            padding: 12px;
            font-size: 16px;
            color: #333;
            border-top: 1px solid #dee2e6;
        }

        th {
            font-weight: bold;
        }
    </style>
</head>

<body>
    <header>
        <nav class="navbar navbar-expand-lg bg-body-tertiary shadow p-3 bg-white rounded">
            <div class="container-fluid">
                <div class="h3">
                    <a class="navbar-brand" href="#">Administration</a>
                </div>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">

                        <li class="nav-item">
                            <a class="nav-link" href="index.php">Thuốc</a>
                        </li>

                        <li class="nav-item">
                            <a class="nav-link active fw-bold" href="indexLoaiThuoc.php">Loại thuốc</a>
                        </li>

                        <li class="nav-item">
                            <a class="nav-link" href="indexNCC.php">Nhà cung cấp</a>
                        </li>

                    </ul>
                </div>
            </div>
        </nav>
    </header>

    <main>
        <div class="container">
            <div class="header">
                <a href="" class=""><i class="bi bi-house"></i></a> <!-- Biểu tượng Home từ Bootstrap Icons -->
                
            </div>

            <div class="form">
                <div class="form-group">
                    <label for="MaLoaiThuoc" >Mã loại thuốc</label>
                    <input type="text" id="MaLoaiThuoc" placeholder="Mã Loại thuốc" class="">
                </div>

                <div class="form-group">
                    <label for="TenLoaiThuoc">Tên loại thuốc</label>
                    <input type="text" id="TenLoaiThuoc" placeholder="Tên loại thuốc">
                </div>
                
                <div class="form-icons d-flex gap-2">
                    <a href="" class="btn"><i class="fa fa-plus-circle"></i></a> <!-- Biểu tượng thêm dữ liệu -->
                    <button class="btn"><i class="fa fa-pencil"></i></button>
                    <button class="btn"><i class="fa fa-trash"></i></button> <!-- Biểu tượng xóa dữ liệu -->
                    <button class="btn"><i class="fa fa-search"></i></button> <!-- Biểu tượng tìm kiếm -->
                </div>
            </div>

            <div class="table-container">
                <table class="table">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Mã loại thuốc</th>
                            <th scope="col">Tên loại thuốc</th>
                            
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Dữ liệu sẽ được thêm vào đây -->
                    </tbody>
                </table>
            </div>
        </div>
    </main>


    <!-- Link Bootstrap JS (Optional) -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
</body>

</html>