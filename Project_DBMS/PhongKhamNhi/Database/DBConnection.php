<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

class DBConnection {
    private $serverName = "localhost";
    private $uid; 
    private $pwd;
    private $database = 'BTL';
    private $conn;

    public function __construct() {
        
        if (isset($_SESSION['username']) && isset($_SESSION['password'])) {
            $this->uid = $_SESSION['username']; 
            $this->pwd = $_SESSION['password']; 
        } else {
            throw new Exception("Chưa có thông tin đăng nhập trong session.");
        }
    }

    public function connect() {
        $this->conn = null;
        try {
            $dsn = "sqlsrv:server=$this->serverName;Database=$this->database;encrypt=true;TrustServerCertificate=true";
            $this->conn = new PDO($dsn, $this->uid, $this->pwd);
            $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch (PDOException $e) {
            return null; 
        }
        return $this->conn;
    }
}
?>
