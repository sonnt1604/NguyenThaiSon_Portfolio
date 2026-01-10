<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Quản Lý Danh Mục Xét Nghiệm</title>
    <link rel="stylesheet" href="../accset/css/bootstrap.min.css">
    <link href="../accset/css/bootstrap-icons/bootstrap-icons.min.css" rel="stylesheet"> 
    <script src="../accset/js/jquery-3.5.1.min.js"></script>
    <script src="../accset/js/popper.min.js"></script>
    <script src="../accset/js/bootstrap.bundle.min.js"></script>
    <style>
        body {
            background: #f5f5f5;
            font-family: 'Varela Round', sans-serif;
            font-size: 13px; 
            margin: 0;
        }

        .navbar {
            background: #435d7d;
            font-size: 18px; 
        }

        .navbar .nav-link {
            color: white; 
        }

        .navbar .nav-link:hover {
            color: white; 
        }

        .table-wrapper {
            background: #fff; 
            padding: 20px; 
            border-radius: 5px; 
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
        }
        .table-title h2 {
            margin: 10px;
            font-size: 30px; 
            text-align: center; 
        }

        .form-container {
            background: #f9f9f8; 
            padding: 20px; 
            border-radius: 5px; 
            margin: 15px 0; 
            box-shadow: 4px 3px 8px rgba(0, 0, 0, 0.4);
        }

        .form-group {
            margin-bottom: 15px; 
        }

        .buttons {
            display: flex;
            justify-content: space-between;
            align-items: center; 
            margin-left: 30px;
            
        }

        .search .btn {
            height: 40px;
            width: 150px;
            margin-left: 5px;
        }
        .search{
            display: flex;
            margin-right: 30px;
        }

        /* Updated styles for the "Thêm" button */
        .btn-primary {
            background-color: #007bff; /* Bootstrap primary color */
            border: none;
            padding: 10px 20px; /* Add some padding */
            font-size: 16px; /* Increase font size */
            border-radius: 5px; /* Round the corners */
            transition: background-color 0.3s; /* Smooth transition */
        }

        .btn-primary:hover {
            background-color: #0056b3; /* Darker shade on hover */
            color: white; /* Ensure text is white on hover */
        }

        table.table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse; 
        }

        table.table th, table.table td {
            padding: 15px; 
            border: 1px solid #e9e9e9; 
        }

        table.table th {
            background: #f8f8f8; 
            text-align: left; 
        }

        td a {
            margin-right: 5px; 
            display: inline-block;
            text-align: center;
        }

        i {
            font-size: 22px; 
        }

        .delete-icon {
            color: #F44336; 
        }

        .edit-icon {
            color: #FFC107;
        }

        .pagination {
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }

        .pagination li {
            list-style: none;
        }

        .pagination li a {
            border: 1px solid #e9e9e9;
            font-size: 14px;
            min-width: 36px;
            min-height: 36px;
            color: #999;
            margin: 0 4px;
            line-height: 36px;
            border-radius: 5px;
            text-align: center;
            padding: 0 10px;
            transition: 0.3s;
        }

        .pagination li a:hover,
        .pagination li a.page-number:hover {
            color: #fff;
            background: #03A9F4;
        }

        .pagination li.active a {
            background: #03A9F4;
            color: #fff;
        }

        .pagination li.active a:hover {
            background: #0397d6;
        }

        .pagination li.disabled a {
            color: #ccc;
            cursor: not-allowed;
        }

        .pagination li i {
            font-size: 16px;
            padding-top: 6px;
        }

        .pagination li a.page-number {
            font-weight: bold;
            color: #333;
        }
    </style>
</head>
<body>
<header>
    <nav class="navbar navbar-expand-lg shadow p-3">
        <div class="container-fluid">

            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item" >
                        <a class="nav-link" href="./index.php">Trang ngoài</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="./index.php?controller=category&action=list">Bệnh Nhân</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="./index.php?controller=author&action=list">Phiếu Khám</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active " href=""> Danh Mục Xét Nghiệm</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</header>
<div class="table-wrapper">
    <div class="table-title">
        <h2>Quản Lý <b>Danh Mục Xét Nghiệm</b></h2>
    </div>
    <div class="form-container">
        <div class="buttons">
            <form action="" method="post" class="d-flex">
                <div class="form-group">
                    <label for="maXetNghiem">Mã Xét Nghiệm:</label>
                    <input type="text" id="maXetNghiem" name="maXetNghiem" class="form-control" required>
                </div>
                <div class="form-group" style="margin-left:25px">
                    <label for="tenXetNghiem">Tên Xét Nghiệm:</label>
                    <input type="text" id="tenXetNghiem" name="tenXetNghiem" class="form-control" required>
                </div>
                <div class="form-group" style="margin-left:25px">
                    <label for="donGia">Đơn Giá:</label>
                    <input type="number" id="donGia" name="donGia" class="form-control" required>
                </div>
                <button type="submit"  style="height:40px;margin:25px" class="btn btn-primary">Thêm</button>
            </form>
            <div class="search">
                <input type="text" class="form-control" placeholder="Nhập tên xét nghiệm...">
                <button class="btn btn-primary">Tìm kiếm</button>
            </div>
        </div>
    </div>
    <table class="table table-striped table-hover">
        <thead>
            <tr>
                <th>MaXetNghiem</th>
                <th>TenXetNghiem</th>
                <th>DonGia</th>
                <th>Hành động</th>       
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Nguyễn Hữu Thành</td>
                <td>123123</td>
                <td>Nguyễn Hữu Thành</td>   
                <td>
                    <a href="">
                        <i class="bi bi-pencil-fill edit-icon"></i>
                    </a>
                    <form action="{{-- route('destroy') , $these->id--}}" method="post" 
                          onsubmit="return confirm('Bạn có chắc chắn muốn xóa mục này?');" 
                          style="display: inline-block; margin-left: 5px;">
                        <button type="submit" style="border: none; background: none; padding: 0; cursor: pointer;">
                            <i class="bi bi-trash3-fill delete-icon"></i>
                        </button>
                    </form>
                </td>
            </tr>
        </tbody>
    </table>
</div>
</body>
</html>
