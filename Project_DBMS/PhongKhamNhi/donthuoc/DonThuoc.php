<?php
session_start(); // Khởi động phiên

// Kiểm tra xem người dùng đã đăng nhập hay chưa
if (!isset($_SESSION['username'])) {
    header("Location: ../index.php"); // Chuyển hướng về trang đăng nhập
    exit();
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prescription Management</title>
    <!-- Bootstrap CSS -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
</head>

<body>
        
    <div class="container mt-5">
        <h2 class="mb-4">Prescription Management</h2>
        <!-- Nav tabs -->
        <ul class="nav nav-tabs" id="myTab" role="tablist">
            <li class="nav-item">
                <a class="nav-link active" id="prescription-tab" data-toggle="tab" href="#prescription" role="tab">Prescriptions</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" id="details-tab" data-toggle="tab" href="#details" role="tab">Prescription Details</a>
            </li>
        </ul>

        <!-- Tab panes -->
        <div class="tab-content mt-3">
            <!-- Prescription List -->
            <div class="tab-pane fade show active" id="prescription" role="tabpanel">
                <h3>Prescription List</h3>
                <form method="GET" action="" class="form-inline mb-3">
                    <div class="input-group">
                        <input type="text" name="search" class="form-control" placeholder="Search by ID" value="<?php echo isset($_GET['search']) ? htmlspecialchars($_GET['search']) : ''; ?>">
                        <div class="input-group-append">
                            <button class="btn btn-primary" type="submit">
                                <i class="fas fa-search"></i>
                            </button>
                        </div>
                    </div>
                </form>
                <a href="add_prescription.php" class="btn btn-primary mb-3">Add New Prescription</a>
                <table class="table table-striped table-bordered">
                    <thead class="thead-dark">
                        <tr>
                            <th>Prescription ID</th>
                            <th>Examination ID</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        // Kết nối đến cơ sở dữ liệu và lấy dữ liệu đơn thuốc
                        require_once '../Database/DBConnection.php';
                        $db = new DBConnection();
                        $conn = $db->connect();

                        // Lấy thông tin tìm kiếm
                        $search = isset($_GET['search']) ? $_GET['search'] : '';
                        if ($search !== '') {
                            $stmt = $conn->prepare("SELECT * FROM donthuoc WHERE MaDon = :search");
                            $stmt->execute(['search' => $search]);
                        } else {
                            $stmt = $conn->prepare("SELECT TOP 15 * FROM donthuoc");
                            $stmt->execute();
                        }
                        $prescriptions = $stmt->fetchAll(PDO::FETCH_ASSOC);

                        foreach ($prescriptions as $prescription) {
                            echo "<tr>
                                <td>" . htmlspecialchars(trim($prescription['MaDon'])) . "</td>
                                <td>" . htmlspecialchars(trim($prescription['MaPhieuKham'])) . "</td>
                                <td>
                                    <a href='edit_prescription.php?id=" . urlencode(trim($prescription['MaDon'])) . "' class='btn btn-warning btn-sm'>Edit</a>
                                    <a href='delete_prescription.php?id=" . urlencode(trim($prescription['MaDon'])) . "' class='btn btn-danger btn-sm' onclick='return confirm(\"Are you sure?\")'>Delete</a>
                                </td>
                            </tr>";
                        }
                        ?>
                    </tbody>
                </table>
            </div>

            <!-- Prescription Details -->
            <div class="tab-pane fade" id="details" role="tabpanel">
                <h3>Prescription Details</h3>
                <table class="table table-striped table-bordered">
                    <thead class="thead-dark">
                        <tr>
                            <th>Prescription ID</th>
                            <th>Medicine ID</th>
                            <th>Quantity</th>
                            <th>Usage</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        // Lấy dữ liệu chi tiết đơn thuốc
                        $stmt_details = $conn->prepare("SELECT TOP 15 * FROM ChiTietDonThuoc");
                        $stmt_details->execute();
                        $details = $stmt_details->fetchAll(PDO::FETCH_ASSOC);

                        foreach ($details as $detail) {
                            echo "<tr>
                                <td>" . htmlspecialchars($detail['MaDon']) . "</td>
                                <td>" . htmlspecialchars($detail['MaThuoc']) . "</td>
                                <td>" . htmlspecialchars($detail['SoLuongBan']) . "</td>
                                <td>" . htmlspecialchars($detail['CachSuDung']) . "</td>
                            </tr>";
                        }
                        ?>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Bootstrap JS and dependencies -->
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>

</html>
