<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Lương nhân viên</title>
    <link rel="stylesheet" href="{{ asset('css/bootstrap.min.css') }}">
    <!-- <link href="{{ asset('css/bootstrap-icons/bootstrap-icons.min.css') }}" rel="stylesheet">  -->
    <link href="{{ asset('css/bootstrap-icons/bootstrap-icons.min.css') }}" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">

    <script src="{{ asset('js/jquery-3.5.1.min.js') }}"></script>
    <script src="{{ asset('js/popper.min.js') }}"></script>
    <script src="{{ asset('js/bootstrap.bundle.min.js') }}"></script>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }

        body {
            background-color: #f0f8ff;
            margin: 0;
            padding: 0;
        }

        .container {
            background-color: #cdeaff;
            padding: 20px;
            border-radius: 8px;
            height: 100vh;
        }

        header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }

        .icon-button {
            background-color: transparent;
            border: none;
            cursor: pointer;
            padding: 0;
            font-size: 1.5em;
            color: #333;
            margin-right: 10px;
        }

        .icon-button:focus {
            outline: none;
        }

        .icon-button:hover {
            color: #0056b3;
        }

        header h1 {
            font-size: 24px;
            color: #333;
        }

        .form-section {
            background-color: #a0cfee;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        .form-row {
            display: flex;
            gap: 20px;
            margin-bottom: 10px;
        }

        .form-row label {
            width: 120px;
            font-weight: bold;
        }

        .form-row input {
            flex: 1;
            padding: 5px;
            border-radius: 4px;
            border: 1px solid #ccc;
            background-color: #e0f7ff;
        }

        .actions {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
        }

        .actions button {
            background-color: transparent;
            border: none;
            cursor: pointer;
            font-size: 1.8em;
            color: #333;
            margin-right: 10px;
        }

        .table-section {
            background-color: #a0cfee;
            padding: 20px;
            border-radius: 8px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;

        }


        table th,
        table td {
            padding: 15px;
            text-align: center;
            border-bottom: 1px solid #ccc;
            word-wrap: break-word;
            
        }

        table th {
            font-weight: bold;
            border-bottom: none;
        }
    </style>

<body>
    <div class="container">
        
        <header>
            
            <div class="logo">
                <button class="icon-button">
                    <i class="bi bi-house-door" aria-label="Home"></i>
                </button>
            </div>

            <h1>LƯƠNG NHÂN VIÊN</h1>

        </header>

        <section class="form-section">
            <div class="form-row">
                <label>Mã nhân viên</label>
                <input type="text">
                <label>Họ tên</label>
                <input type="text">
                <label>Thời gian (tháng/năm)</label>
                <input type="month">
                
            </div>
            <div class="form-row">
                <label>Ngày sinh</label>
                <input type="date">
                <label>Số điện thoại</label>
                <input type="text">
                <label>Chức vụ</label>
                <input type="text">
            </div>
            <div class="form-row">
                <label>Số ngày công</label>
                <input type="text">
                <label>Mức lương</label>
                <input type="text">
                <label>Phụ cấp</label>
                <input type="text">
            </div>
            <div class="actions">
                <button><i class="bi bi-trash3" alt="Edit"></i></button>
                <button><i class="bi bi-pencil-square" alt="Edit"></i></button>
                <button><i class="bi bi-search" alt="Search"> </i></button>
                <button><i class="bi bi-printer" alt="Print"> </i></button>

            </div>
        </section>

        <section class="table-section">
            <table>
                <thead>
                    <tr>
                        <th>Mã nhân viên</th>
                        <th>Họ tên</th>
                        <th>Thời gian (tháng/năm)</th>
                        <th>Mức lương</th>
                        <th>Số ngày công</th>
                        <th>Phụ cấp</th>
                        <th>Phạt</th>
                        <th>Tổng</th>
                    </tr>
                </thead>
                <tbody>
                    
                </tbody>
            </table>
        </section>
    </div>
</body>

</html>