USE master;
ALTER DATABASE BTL SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
DROP DATABASE BTL;
CREATE DATABASE BTL;
USE BTL
GO
-- 1. Bảng Xét nghiệm
CREATE TABLE DanhMucXetNghiem (
    MaXetNghiem VARCHAR(50) PRIMARY KEY,
    TenXetNghiem NVARCHAR(255),
    DonGia MONEY
);

-- 2. Bảng Bệnh nhân
CREATE TABLE BenhNhan (
    MaBenhNhan VARCHAR(50) PRIMARY KEY,
    TenBenhNhan NVARCHAR(255),
    GioiTinh NVARCHAR(50),
    NgaySinh DATE,
    TenNguoiThan NVARCHAR(255),
    SoCCCDNguoiThan VARCHAR(50),
    DiaChi NVARCHAR(255),
    SoDienThoai VARCHAR(50),
    NgayHenKham DATE
);

-- 3. Bảng Nhân viên (được tạo trước vì có nhiều bảng tham chiếu tới)
CREATE TABLE NhanVien (
    MaNhanVien VARCHAR(50) PRIMARY KEY,
    HoTen NVARCHAR(255),
    NgaySinh DATE,
    GioiTinh NVARCHAR(50),
    DiaChi NVARCHAR(255),
    SoDienThoai VARCHAR(50),
    SoCCCD VARCHAR(50),
    TrinhDo NVARCHAR(50),
    ChucVu NVARCHAR(50),
    NgayVaoLam DATE,
    MucLuong INT,
    PhuCap INT
);

-- 4. Bảng Phiếu khám
CREATE TABLE PhieuKham (
    MaPhieuKham VARCHAR(50) PRIMARY KEY,
    MaBenhNhan VARCHAR(50) FOREIGN KEY REFERENCES BenhNhan(MaBenhNhan),
    MaNhanVien VARCHAR(50) FOREIGN KEY REFERENCES NhanVien(MaNhanVien),
    LyDoKhamBenh NVARCHAR(255),
    ChuanDoan NVARCHAR(255),
    NgayLamPhieu DATE,
    KetLuan NVARCHAR(255)
);

-- 5. Bảng Phiếu xét nghiệm
CREATE TABLE PhieuXetNghiem (
    MaPhieuXetNghiem VARCHAR(50) PRIMARY KEY,
    MaPhieuKham VARCHAR(50) FOREIGN KEY REFERENCES PhieuKham(MaPhieuKham),
    MaNhanVien VARCHAR(50) FOREIGN KEY REFERENCES NhanVien(MaNhanVien),
    MaXetNghiem VARCHAR(50) FOREIGN KEY REFERENCES DanhMucXetNghiem(MaXetNghiem),
    NoiDungXetNghiem NVARCHAR(255),
    KetQuaXetNghiem NVARCHAR(255)
);

-- 6. Bảng Tài khoản
CREATE TABLE TaiKhoan (
    SoTaiKhoan VARCHAR(50) PRIMARY KEY,
    MaNhanVien VARCHAR(50) FOREIGN KEY REFERENCES NhanVien(MaNhanVien),
    TenDangNhap VARCHAR(50),
    MatKhau VARCHAR(50)
);

-- 7. Bảng Đơn thuốc
CREATE TABLE DonThuoc (
    MaDon VARCHAR(50) PRIMARY KEY,
    MaPhieuKham VARCHAR(50) FOREIGN KEY REFERENCES PhieuKham(MaPhieuKham)
);

-- 8. Bảng Loại thuốc
CREATE TABLE LoaiThuoc (
    MaLoaiThuoc VARCHAR(50) PRIMARY KEY,
    TenLoaiThuoc NVARCHAR(255)
);

-- 9. Bảng Nhà cung cấp
CREATE TABLE NhaCungCap (
    MaNCC VARCHAR(50) PRIMARY KEY,
    TenNCC NVARCHAR(255),
    DiaChi NVARCHAR(255),
    TinhTrang NVARCHAR(255)
);

-- 10. Bảng Thuốc
CREATE TABLE Thuoc (
    MaThuoc VARCHAR(50) PRIMARY KEY,
    MaLoaiThuoc VARCHAR(50) FOREIGN KEY REFERENCES LoaiThuoc(MaLoaiThuoc),
    TenThuoc NVARCHAR(255),
    GiaThuoc MONEY,
    ThanhPhanChinh NVARCHAR(255),
    SoLuongThuocTrongKho INT,
    CachSuDung NVARCHAR(255),
    MaNCC VARCHAR(50) FOREIGN KEY REFERENCES NhaCungCap(MaNCC)
);

-- 11. Bảng Chi tiết đơn thuốc
CREATE TABLE ChiTietDonThuoc (
    MaDon VARCHAR(50) FOREIGN KEY REFERENCES DonThuoc(MaDon),
    MaThuoc VARCHAR(50) FOREIGN KEY REFERENCES Thuoc(MaThuoc),
    SoLuongBan INT,
    CachSuDung NVARCHAR(255)
);

-- 12. Bảng Lương nhân viên
CREATE TABLE LuongNhanVien (
    MaNhanVien VARCHAR(50) FOREIGN KEY REFERENCES NhanVien(MaNhanVien),
    Thang INT,
    Nam INT,
    SoNgayCong FLOAT
);