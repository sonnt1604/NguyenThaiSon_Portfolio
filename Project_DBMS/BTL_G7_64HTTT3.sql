----Nhóm 7 Lớp 64HTT3----
use BTL
----Hoàng Yến Nhi STT:37 ----
--- Thủ tục---
--Viết thủ tục đưa ra thông tin các loại xét nghiệm và số lần thực hiện xét nghiệm của loại đó (MaXetNghiem, TenXetNghiem, SolanXetNghiem).(NHI)
DROP PROCEDURE LietKeBenhNhan

CREATE PROCEDURE ThongTinXetNghiem
AS
BEGIN
    SELECT xn.MaXetNghiem, xn.TenXetNghiem, COUNT(pxn.MaPhieuXetNghiem) AS SoLanXetNghiem
    FROM DanhMucXetNghiem xn
    LEFT JOIN PhieuXetNghiem pxn ON xn.MaXetNghiem = pxn.MaXetNghiem
    GROUP BY xn.MaXetNghiem, xn.TenXetNghiem;
END;
EXEC ThongTinXetNghiem
DROP PROCEDURE ThongTinXetNghiem

---Viết thủ tục trả về danh sách các bệnh nhân đã khám bệnh trong một khoảng thời gian cụ thể, với đầu vào 
---là 1 khoảng thời gian (MaBenhNhan, TenBenhNhan, GioiTinh, NgaySinh, TenNguoiThan, SoCCCDNguoiThan, DiaChi, SoDienThoai, 
---LyDoKhamBenh, ChuanDoan, NgayLamPhieu, KetLuan)
CREATE PROCEDURE LietKeBenhNhan(@startDate DATE = NULL, @endDate DATE = NULL)
AS
BEGIN
  SELECT bn.MaBenhNhan, bn.TenBenhNhan, bn.GioiTinh, bn.NgaySinh, bn.TenNguoiThan, 
         bn.SoCCCDNguoiThan, bn.DiaChi, bn.SoDienThoai, pk.LyDoKhamBenh, pk.ChuanDoan, pk.NgayLamPhieu, pk.KetLuan
  FROM BenhNhan bn
  JOIN PhieuKham pk ON bn.MaBenhNhan = pk.MaBenhNhan
  WHERE (@startDate IS NULL OR pk.NgayLamPhieu >= @startDate)
  AND (@endDate IS NULL OR pk.NgayLamPhieu <= @endDate);
END;

EXEC LietKeBenhNhan ;
EXEC LietKeBenhNhan @startDate='2024-10-10' ,@endDate='2024-10-12';
EXEC LietKeBenhNhan @startDate='2024-10-15';
EXEC LietKeBenhNhan @endDate='2024-10-09';
---View----
---Viết view để hiển thị thông tin bệnh nhân, kết quả xét nghiệm và đơn thuốc của bệnh nhân (đơn thuốc) 
---(MaBenhNhan, TenBenhNhan, GioiTinh, DiaChi, MaPhieuXetNghiem, TenXetNghiem, KetQuaXetNghiem, MaDon, MaThuoc, TenThuoc)
DROP VIEW ThongTinBenhNhanXetNghiemDonThuoc;

CREATE VIEW ThongTinBenhNhanXetNghiemDonThuoc
AS
SELECT bn.MaBenhNhan, bn.TenBenhNhan, bn.GioiTinh, bn.DiaChi, 
       pxn.MaPhieuXetNghiem, xn.TenXetNghiem, pxn.KetQuaXetNghiem, 
       dt.MaDon, mdt.MaThuoc, t.TenThuoc
FROM BenhNhan bn
JOIN PhieuKham pk ON bn.MaBenhNhan = pk.MaBenhNhan
JOIN PhieuXetNghiem pxn ON pk.MaPhieuKham = pxn.MaPhieuKham
JOIN DanhMucXetNghiem xn ON pxn.MaXetNghiem = xn.MaXetNghiem
JOIN DonThuoc dt ON pk.MaPhieuKham = dt.MaPhieuKham
JOIN ChiTietDonThuoc mdt ON dt.MaDon = mdt.MaDon
JOIN Thuoc t ON mdt.MaThuoc = t.MaThuoc;

SELECT * From ThongTinBenhNhanXetNghiemDonThuoc

---Hàm
--Viết hàm tính doanh thu một ngày bất kỳ.
CREATE FUNCTION DoanhThuNgay (@ngay DATE)
RETURNS MONEY
AS
BEGIN
    DECLARE @tien MONEY;
    
    SELECT @tien = SUM(dm.DonGia) + SUM(ct.SoLuongBan * t.GiaThuoc)
    FROM PhieuKham pk
    JOIN PhieuXetNghiem px ON pk.MaPhieuKham = px.MaPhieuKham
    JOIN DanhMucXetNghiem dm ON px.MaXetNghiem = dm.MaXetNghiem
    JOIN DonThuoc dt ON pk.MaPhieuKham = dt.MaPhieuKham
    JOIN ChiTietDonThuoc ct ON dt.MaDon = ct.MaDon
    JOIN Thuoc t ON ct.MaThuoc = t.MaThuoc
    WHERE pk.NgayLamPhieu = @ngay
    GROUP BY pk.NgayLamPhieu;
    
    RETURN @tien;
END;
DROP FUNCTION DoanhThuNgay ;
SELECT * FROM PhieuKham
SELECT dbo.DoanhThuNgay('2024-09-09') AS DoanhThu;

---Trigger
--Viết trigger để khi thêm, xóa số lượng trong bảng  CHITIETDONTHUOC thì số lượng tồn trong bảng THUOC  cập nhật theo 
create trigger SLTonThuocThem
on ChiTietDonThuoc
for insert
as
Begin
     if ((select SoLuongThuocTrongKho from THUOC 
	 where MaThuoc = (select MaThuoc from inserted)) >= (select SoLuongBan from inserted))
     Begin
          update THUOC
          set SoLuongThuocTrongKho =  SoLuongThuocTrongKho - (select SoLuongban from inserted) 
		  where THUOC.MaThuoc = (select MaThuoc from inserted)
          print N'Thêm thành công'
     End
     else
     Begin
          print N'Số lượng thuốc trong kho không đủ'
		  rollback tran
     End
End
DROP Trigger SLTonThuocThem
SELECT * FROM ChiTietDonThuoc Where MaDon = '1000'
SELECT * FROM DonThuoc 
SELECT * FROM Thuoc Where MaThuoc ='29'
--  (trường hợp đủ thuốc)
INSERT INTO CHITIETDONTHUOC (MaDon, MaThuoc, SoLuongBan, CachSuDung) 
VALUES ('20', '72', 10, N'Sử dụng mỗi ngày 2 lần');

--  (trường hợp không đủ thuốc)
INSERT INTO CHITIETDONTHUOC (MaDon, MaThuoc, SoLuongBan, CachSuDung) 
VALUES ('1000', '29', 90, N'Uống sau khi ăn');
---
create trigger SLTonThuocXoa
on ChiTietDonThuoc
for delete
as
Begin
     update THUOC
	 set SoLuongThuocTrongKho = SoLuongThuocTrongKho + (select SoLuongban from deleted)
	 where THUOC.MaThuoc = (select MaThuoc from deleted)
	 print N'Xóa thành công'
End
SELECT * FROM ChiTietDonThuoc Where MaDon = '100'
SELECT * FROM Thuoc Where MaThuoc ='20'
DELETE FROM CHITIETDONTHUOC WHERE MaDon = '100' AND MaThuoc = '20';






----Nguyễn Tuấn Phước STT:40----
----View----
----thống kê tổng số lượt kê đơn và tổng số thuốc đã được kê đơn cho mỗi loại thuốc (MaLoaiThuoc, TenLoaiThuoc, SoLuotKeDon, TongSoLuongThuoc)----
DROP VIEW ThongKeKeDon;

CREATE VIEW ThongKeKeDon AS
SELECT 
    lt.MaLoaiThuoc,
    lt.TenLoaiThuoc,
    COUNT( dt.MaDon) AS SoLuotKeDon,
    SUM(ct.SoLuongBan) AS TongSoLuongThuoc
FROM 
    LoaiThuoc lt
LEFT JOIN 
    Thuoc t ON lt.MaLoaiThuoc = t.MaLoaiThuoc
LEFT JOIN 
    ChiTietDonThuoc ct ON t.MaThuoc = ct.MaThuoc
LEFT JOIN 
    DonThuoc dt ON ct.MaDon = dt.MaDon
GROUP BY 
    lt.MaLoaiThuoc, lt.TenLoaiThuoc;
	
-- tong so luot ke don 
select Sum(SoLuotKeDon) as tong
FROM
	ThongKeKeDon

Select * from ThongKeKeDon;

----Thủ tục----
--tổng số lượt kê đơn và tổng số thuốc đã được kê đơn cho 1 loại thuốc (MaLoaiThuoc, TenLoaiThuoc, SoLuotKeDon, TongSoLuongThuoc) đầu vào là mã loại thuốc
DROP PROCEDURE ProcThongKeKeDon;

CREATE PROCEDURE ProcThongKeKeDon
    @MaLoaiThuocInput VARCHAR(50)
AS
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM LoaiThuoc lt
        WHERE lt.MaLoaiThuoc = @MaLoaiThuocInput
    )
    BEGIN
        PRINT 'Khong tim thay thuoc co ma: ' + @MaLoaiThuocInput;
        RETURN;  
    END
    SELECT 
        lt.MaLoaiThuoc,
        lt.TenLoaiThuoc,
        COUNT(dt.MaDon) AS SoLuotKeDon,
         SUM(ct.SoLuongBan) AS TongSoLuongThuoc
    FROM 
        LoaiThuoc lt
    LEFT JOIN 
        Thuoc t ON lt.MaLoaiThuoc = t.MaLoaiThuoc
    LEFT JOIN 
        ChiTietDonThuoc ct ON t.MaThuoc = ct.MaThuoc
    LEFT JOIN 
        DonThuoc dt ON ct.MaDon = dt.MaDon
    WHERE 
        lt.MaLoaiThuoc = @MaLoaiThuocInput
    GROUP BY  
        lt.MaLoaiThuoc, lt.TenLoaiThuoc;
END;
EXEC ProcThongKeKeDon  'H000' ;
exec ProcThongKeKeDon 'LT001';
----Hàm----
----Viết hàm thống kê tổng số lượt kê đơn và tổng số thuốc cho mỗi loại thuốc----
DROP FUNCTION FuncThongKeKeDon;

CREATE FUNCTION FuncThongKeKeDon()
RETURNS @ThongKeKeDon TABLE (
    MaLoaiThuoc VARCHAR(50),
    TenLoaiThuoc NVARCHAR(255),
    SoLuotKeDon INT,
    TongSoLuongThuoc INT
)
AS
BEGIN
    INSERT INTO @ThongKeKeDon
    SELECT 
        lt.MaLoaiThuoc,
        lt.TenLoaiThuoc,
        COUNT(dt.MaDon) AS SoLuotKeDon,
        SUM(ct.SoLuongBan) AS TongSoLuongThuoc
    FROM 
        LoaiThuoc lt
    LEFT JOIN 
        Thuoc t ON lt.MaLoaiThuoc = t.MaLoaiThuoc
    LEFT JOIN 
        ChiTietDonThuoc ct ON t.MaThuoc = ct.MaThuoc
    LEFT JOIN 
        DonThuoc dt ON ct.MaDon = dt.MaDon
    GROUP BY 
        lt.MaLoaiThuoc, lt.TenLoaiThuoc;
    RETURN;
END;
SELECT * FROM FuncThongKeKeDon();

-- trung bình tổng số lượng bán thuốc của những thuốc có tổng số lượng != null 
SELECT AVG(TongSoLuongThuoc) as TbSoLuongThuoc
FROM FuncThongKeKeDon()
WHERE TongSoLuongThuoc > 0


----Trigger----
-----Viết 1 trigger không cho phép thêm vào bảng CHITIETDONTHUOC nếu SoLuongBan < 0----
drop trigger trg_ChiTietDonThuoc

CREATE TRIGGER trg_ChiTietDonThuoc
ON ChiTietDonThuoc	
FOR INSERT
AS
BEGIN
    IF EXISTS (SELECT 1 
			FROM inserted 
			WHERE SoLuongBan < 0)
    BEGIN
		print N'Số lượng bán phải lớn hơn 0';
        ROLLBACK TRANSACTION;
    END
END;

INSERT INTO ChiTietDonThuoc (MaDon, MaThuoc, SoLuongBan, CachSuDung)
VALUES ('1', '16', -5, 'uong sau an');

INSERT INTO ChiTietDonThuoc (MaDon, MaThuoc, SoLuongBan, CachSuDung)
VALUES ('1', '16', 10, 'uong sau an');

SELECT * FROM ChiTietDonThuoc
WHERE MaDon = '1' ANd MaThuoc = '16';



----Trần Anh Quân STT:42----
----View----
--viết một view trả về doanh thu theo tháng của phòng khám
CREATE VIEW DoanhThuTheoThang AS
SELECT 
    MONTH(PK.NgayLamPhieu) AS Thang,
    YEAR(PK.NgayLamPhieu) AS Nam,
    SUM(T.GiaThuoc * CT.SoLuongBan) AS DoanhThu
FROM Thuoc T
JOIN ChiTietDonThuoc CT ON T.MaThuoc = CT.MaThuoc
JOIN DonThuoc D ON CT.MaDon = D.MaDon
JOIN PhieuKham PK ON D.MaPhieuKham = PK.MaPhieuKham
GROUP BY MONTH(PK.NgayLamPhieu), YEAR(PK.NgayLamPhieu);

SELECT * FROM DoanhThuTheoThang order by Thang;

--dựa trên view tính doanh thu của cả năm 2024
SELECT Nam, SUM(DoanhThu) as TongDoanhThu 
FROM DoanhThuTheoThang 
WHERE Nam = 2024
GROUP BY Nam

----Thủ tục----
--viết một thủ tục tính doanh thu một năm với đầu vào là một năm
CREATE PROC DOANHTHUNAM (@Year INT)
AS
BEGIN
    SELECT @Year AS Nam, SUM(T.GiaThuoc * CT.SoLuongBan) AS DoanhThu
    FROM Thuoc T
    JOIN ChiTietDonThuoc CT ON T.MaThuoc = CT.MaThuoc
    JOIN DonThuoc D ON CT.MaDon = D.MaDon
    JOIN PhieuKham PK ON D.MaPhieuKham = PK.MaPhieuKham
    WHERE YEAR(PK.NgayLamPhieu) = @Year;
END;

EXEC DOANHTHUNAM 2024;
----Hàm----
-- Viết hàm tính tổng tiền thuốc của một bệnh nhân
CREATE FUNCTION TinhTongTienThuoc(@MaBenhNhan VARCHAR(50))
RETURNS MONEY
AS
BEGIN
    DECLARE @TongTienThuoc MONEY;

    SELECT @TongTienThuoc = SUM(T.GiaThuoc * CTDT.SoLuongBan)
    FROM BenhNhan BN
    JOIN PhieuKham PK ON BN.MaBenhNhan = PK.MaBenhNhan
    JOIN DonThuoc DT ON PK.MaPhieuKham = DT.MaPhieuKham
    JOIN ChiTietDonThuoc CTDT ON DT.MaDon = CTDT.MaDon
    JOIN Thuoc T ON CTDT.MaThuoc = T.MaThuoc
    WHERE BN.MaBenhNhan = @MaBenhNhan;

    RETURN @TongTienThuoc;
END;

-- Kiểm tra hàm TinhTongTienThuoc
SELECT dbo.TinhTongTienThuoc('5') AS TongTienThuoc;

--Hàm tính doanh thu trong một khoảng thời gian (với đầu vào là khoảng thời gian)
CREATE FUNCTION TinhDoanhThu(@NgayBatDau DATE, @NgayKetThuc DATE)
RETURNS MONEY
AS
BEGIN
    DECLARE @DoanhThu MONEY;

    SELECT @DoanhThu = SUM(T.GiaThuoc * CTDT.SoLuongBan)
    FROM PhieuKham PK
    JOIN DonThuoc DT ON PK.MaPhieuKham = DT.MaPhieuKham
    JOIN ChiTietDonThuoc CTDT ON DT.MaDon = CTDT.MaDon
    JOIN Thuoc T ON CTDT.MaThuoc = T.MaThuoc
    WHERE PK.NgayLamPhieu BETWEEN @NgayBatDau AND @NgayKetThuc;

    RETURN @DoanhThu;
END;

-- Kiểm tra hàm TinhDoanhThu
SELECT dbo.TinhDoanhThu('2023-12-01', '2023-12-31') AS DoanhThu

-- Liệt kê doanh thu của các tháng có doanh thu lớn hơn tháng 12
DECLARE @DoanhThuThang12 MONEY;
SET @DoanhThuThang12 = dbo.TinhDoanhThu('2023-12-01', '2023-12-31');

SELECT 
    MONTH(PK.NgayLamPhieu) AS Thang,
    YEAR(PK.NgayLamPhieu) AS Nam,
    SUM(T.GiaThuoc * CTDT.SoLuongBan) AS DoanhThu
FROM 
    PhieuKham PK
    JOIN DonThuoc DT ON PK.MaPhieuKham = DT.MaPhieuKham
    JOIN ChiTietDonThuoc CTDT ON DT.MaDon = CTDT.MaDon
    JOIN Thuoc T ON CTDT.MaThuoc = T.MaThuoc
GROUP BY 
    MONTH(PK.NgayLamPhieu), YEAR(PK.NgayLamPhieu)
HAVING 
    SUM(T.GiaThuoc * CTDT.SoLuongBan) > @DoanhThuThang12;


----Trigger----
--Trigger để không cho phép thêm bản ghi vào bảng  LUONGNHANVIEN nếu tháng và năm lớn hơn tháng và  năm hiện tại
CREATE TRIGGER trg_CheckLuongNhanVienDate
ON LuongNhanVien
INSTEAD OF INSERT
AS
BEGIN
    DECLARE @CurrentMonth INT, @CurrentYear INT;
    SET @CurrentMonth = MONTH(GETDATE());
    SET @CurrentYear = YEAR(GETDATE());

    IF EXISTS (
        SELECT 1
        FROM inserted
        WHERE 
            (Thang < 1 OR Thang > 12) OR
            (Thang > @CurrentMonth AND Nam >= @CurrentYear) OR 
            (Nam > @CurrentYear)
    )
    BEGIN
        RAISERROR('Không thể thêm bản ghi vào bảng LuongNhanVien với tháng và năm không hợp lệ hoặc lớn hơn tháng và năm hiện tại.', 16, 1);
        ROLLBACK TRANSACTION;
    END
    ELSE
    BEGIN
        INSERT INTO LuongNhanVien (MaNhanVien, Thang, Nam, SoNgayCong)
        SELECT MaNhanVien, Thang, Nam, SoNgayCong
        FROM inserted;
    END
END;


-- Kiểm tra trigger
select * from LuongNhanVien where MaNhanVien = '23'

INSERT INTO LuongNhanVien (MaNhanVien, Thang, Nam, SoNgayCong)
VALUES ('23', MONTH(GETDATE()), YEAR(GETDATE()), 20);

INSERT INTO LuongNhanVien (MaNhanVien, Thang, Nam, SoNgayCong)
VALUES ('11', 16, 2021, 20); 

INSERT INTO LuongNhanVien (MaNhanVien, Thang, Nam, SoNgayCong)
VALUES ('19', 10, 2026, 20); 



----Nguyễn Thái Sơn STT:43----
----View----
-- Viết view để hiển thị thông tin của bệnh nhân, tổng số tiền khám bệnh (xét nghiệm và thuốc) của bệnh nhân (phiếu thu) (TenBenhNhan, TongTienXetNghiem, TongTienThuoc)
CREATE VIEW PhieuThu 
AS
SELECT BenhNhan.TenBenhNhan, 
	SUM(DanhMucXetNghiem.DonGia) AS TongTienXetNghiem, 
	SUM(ChiTietDonThuoc.SoLuongBan * Thuoc.GiaThuoc) AS TongTienThuoc
FROM BenhNhan
INNER JOIN PhieuKham ON BenhNhan.MaBenhNhan = PhieuKham.MaBenhNhan
INNER JOIN PhieuXetNghiem ON PhieuKham.MaPhieuKham = PhieuXetNghiem.MaPhieuKham
INNER JOIN DanhMucXetNghiem ON PhieuXetNghiem.MaXetNghiem = DanhMucXetNghiem.MaXetNghiem
INNER JOIN DonThuoc ON PhieuKham.MaPhieuKham = DonThuoc.MaPhieuKham
INNER JOIN ChiTietDonThuoc ON DonThuoc.MaDon = ChiTietDonThuoc.MaDon
INNER JOIN Thuoc ON ChiTietDonThuoc.MaThuoc = Thuoc.MaThuoc
GROUP BY BenhNhan.TenBenhNhan;

----Thủ tục----
-- Viết thủ tục để tính số lượng thuốc còn trong kho
CREATE PROC SoLuongThuocConTrongKho
    @MaThuoc VARCHAR(50) = NULL 
AS
BEGIN
IF @MaThuoc IS NULL
    BEGIN
        SELECT Thuoc.MaThuoc, Thuoc.TenThuoc, Thuoc.SoLuongThuocTrongKho, ChiTietDonThuoc.SoLuongBan,
		 Thuoc.SoLuongThuocTrongKho - SUM(ChiTietDonThuoc.SoLuongBan)  AS SoLuongConLai
        FROM Thuoc INNER JOIN ChiTietDonThuoc ON Thuoc.MaThuoc = ChiTietDonThuoc.MaThuoc
		GROUP BY Thuoc.MaThuoc, Thuoc.TenThuoc,ChiTietDonThuoc.SoLuongBan, Thuoc.SoLuongThuocTrongKho
    END
ELSE
    BEGIN
        SELECT Thuoc.MaThuoc, Thuoc.TenThuoc, Thuoc.SoLuongThuocTrongKho, ChiTietDonThuoc.SoLuongBan,
		 Thuoc.SoLuongThuocTrongKho - SUM(ChiTietDonThuoc.SoLuongBan)  AS SoLuongConLai
        FROM Thuoc INNER JOIN ChiTietDonThuoc ON Thuoc.MaThuoc = ChiTietDonThuoc.MaThuoc
        WHERE Thuoc.MaThuoc = @MaThuoc
		GROUP BY Thuoc.MaThuoc, Thuoc.TenThuoc, ChiTietDonThuoc.SoLuongBan, Thuoc.SoLuongThuocTrongKho
	END
END

----Hàm----
--Viết một hàm trả về danh sách bệnh nhân đã tham gia một loại xét nghiệm y tế
CREATE FUNCTION fn_BenhNhanThamGiaXetNghiem (
    @MaXetNghiem VARCHAR(50)
)
RETURNS TABLE
AS
RETURN 
(
    SELECT BenhNhan.MaBenhNhan, BenhNhan.TenBenhNhan, BenhNhan.GioiTinh, BenhNhan.NgaySinh, BenhNhan.DiaChi, BenhNhan.SoDienThoai, PhieuXetNghiem.MaXetNghiem
    FROM BenhNhan 
	JOIN PhieuKham ON BenhNhan.MaBenhNhan = PhieuKham.MaBenhNhan
    JOIN PhieuXetNghiem ON PhieuKham.MaPhieuKham = PhieuXetNghiem.MaPhieuKham
    WHERE PhieuXetNghiem.MaXetNghiem = @MaXetNghiem
);
----Trigger----
----viết 1 trigger không cho phép thêm bản ghi vào bảng bệnh nhân nếu ngày hẹn khám nhỏ hơn ngày hiện tại hoặc ngày hẹn khám lớn hơn ngày hiện tại quá 7 ngày
CREATE TRIGGER kiemtra_ngayhenkham
ON BenhNhan
INSTEAD OF INSERT
AS
BEGIN
    DECLARE @NgayHenKham DATE;
    DECLARE @NgayHienTai DATE = GETDATE();

    SELECT @NgayHenKham = NgayHenKham FROM inserted;

    IF @NgayHenKham < @NgayHienTai OR @NgayHenKham > DATEADD(DAY, 7, @NgayHienTai)
    BEGIN
        PRINT N'Ngày hẹn khám không hợp lệ. Ngày hẹn phải từ hôm nay đến trong vòng 7 ngày.';
    END
    ELSE
    BEGIN
        INSERT INTO BenhNhan
        SELECT * FROM inserted;
		
		Print N'Thêm bệnh nhân thành công'
    END
END;



----Nguyễn Hữu Thành STT:48----

----View--- 
----Thống kê số tiền đã xét nghiệm, số tiền đã mua thuốc, tổng tiền,
----số lần tới khám của bệnh nhân (MaBenhNhan, TenBenhNhan, GioiTinh, NgaySinh, TenNguoiThan, 
----SoDienThoai, DiaChi, TienThuoc, TienXetNghiem, TongTien, SoLanKham)
IF EXISTS (SELECT * FROM sys.views WHERE object_id = OBJECT_ID('dbo.ThongKeBN'))
BEGIN
    DROP VIEW dbo.ThongKeBN;
END;

CREATE VIEW ThongKeBN
AS
    SELECT MaBenhNhan,
           TenBenhNhan,
           GioiTinh,
           NgaySinh,
           TenNguoiThan,
           SoDienThoai,
           DiaChi,
           dbo.TienThuoc(MaBenhNhan) AS TienThuoc,
           dbo.TienXetNghiem(MaBenhNhan) AS TienXetNghiem,
           (dbo.TienThuoc(MaBenhNhan) + dbo.TienXetNghiem(MaBenhNhan)) AS TongTien,
           dbo.SoLanKham(MaBenhNhan) AS SolanKham
    FROM BenhNhan;

SELECT * FROM ThongKeBN where DiaChi = 'HaiPhong' order by CAST(MaBenhNhan AS INT) ;
---đưa ra tổng tiền thu được từ các bệnh nhân nữ--
Select sum(TongTien) as TongDoanhThu
	From ThongKeBN
	where GioiTinh = 'Nu'

----Thủ tục----
----Viết thủ tục để tính tổng chi phí cho một phiếu khám bệnh (bao gồm cả chi phí của các xét nghiệm và chi phí thuốc)--
IF OBJECT_ID('dbo.TinhTongChiPhiPhieuKham', 'P') IS NOT NULL
BEGIN
    DROP PROCEDURE dbo.TinhTongChiPhiPhieuKham;
END;
CREATE PROC TinhTongChiPhiPhieuKham
    @MaPhieuKham VARCHAR(10),
    @TongChiPhi MONEY OUTPUT
AS
BEGIN
    SELECT @TongChiPhi = SUM(DMXN.DonGia)
    FROM PhieuKham PK
    INNER JOIN PhieuXetNghiem PXN ON PK.MaPhieuKham = PXN.MaPhieuKham
    INNER JOIN DanhMucXetNghiem DMXN ON PXN.MaXetNghiem = DMXN.MaXetNghiem
    WHERE PK.MaPhieuKham = @MaPhieuKham;
    SELECT @TongChiPhi = @TongChiPhi + SUM(T.GiaThuoc * CTDON.SoLuongBan)
    FROM PhieuKham PK
    INNER JOIN DonThuoc DT ON PK.MaPhieuKham = DT.MaPhieuKham
    INNER JOIN ChiTietDonThuoc CTDON ON DT.MaDon = CTDON.MaDon
    INNER JOIN Thuoc T ON CTDON.MaThuoc = T.MaThuoc
    WHERE PK.MaPhieuKham = @MaPhieuKham;
END;

DECLARE @TongChiPhi MONEY;
DECLARE @MaPhieuKham VARCHAR(10) = '2';  
EXEC TinhTongChiPhiPhieuKham @MaPhieuKham, @TongChiPhi OUTPUT;
SELECT @TongChiPhi AS TongChiPhi;


----Hàm----
----Hàm tính tổng tiền xét nghiệm của một bệnh nhân.
IF OBJECT_ID('dbo.TienXetNghiem', 'FN') IS NOT NULL
BEGIN
    DROP FUNCTION dbo.TienXetNghiem;
END;
CREATE FUNCTION dbo.TienXetNghiem(@MaBenhNhan VARCHAR(50)) 
RETURNS MONEY
AS
BEGIN
    DECLARE @TongTienXetNghiem MONEY;

    SELECT @TongTienXetNghiem = SUM(DMXN.DonGia)
    FROM BenhNhan BN
    INNER JOIN PhieuKham PK ON BN.MaBenhNhan = PK.MaBenhNhan
    INNER JOIN PhieuXetNghiem PXN ON PK.MaPhieuKham = PXN.MaPhieuKham
    INNER JOIN DanhMucXetNghiem DMXN ON PXN.MaXetNghiem = DMXN.MaXetNghiem
    WHERE BN.MaBenhNhan = @MaBenhNhan;

    RETURN ISNULL(@TongTienXetNghiem, 0);
END;

---tính tổng tiền xét nghiệm của 1 bệnh nhân
SELECT dbo.TienXetNghiem('2') AS TongTienXetNghiem;
----Hiển thị tổng tiền xet nghiệm cho tất cả bệnh nhân
SELECT 
    BN.MaBenhNhan, 
    BN.TenBenhNhan, 
    dbo.TienXetNghiem(BN.MaBenhNhan) AS TongTienXetNghiem
FROM BenhNhan BN;
----hiển thị cách bệnh nhân có tổng tiền xét nghiệm >1.000.000
SELECT 
    BN.MaBenhNhan, 
    BN.TenBenhNhan, 
    dbo.TienXetNghiem(BN.MaBenhNhan) AS TongTienXetNghiem
FROM BenhNhan BN
WHERE dbo.TienXetNghiem(BN.MaBenhNhan) > 1000000;

----Kiểm tra xem bệnh nhân có xét nghiệm không
SELECT 
    BN.MaBenhNhan, 
    BN.TenBenhNhan,
	dbo.TienXetNghiem(BN.MaBenhNhan) AS TongTienXetNghiem
FROM BenhNhan BN
WHERE dbo.TienXetNghiem(BN.MaBenhNhan) = 0;

----đưa ra danh sách bệnh nhân cso tổng tiền xét nghiệm lớn hơn bằng tổng tiền xét nghiệm đc trả ra bởi hàm
SELECT 
    BN.MaBenhNhan, 
    BN.TenBenhNhan,
	dbo.TienXetNghiem(BN.MaBenhNhan) AS TongTienXetNghiem
FROM BenhNhan BN
WHERE dbo.TienXetNghiem(BN.MaBenhNhan) >= dbo.TienXetNghiem('2');


----Trigger----
------ Viết trigger cập nhật Phụ cấp trong bảng NHANVIEN 
-----• Nếu nhân viên có Trình độ Thạc sĩ thì Phụ cấp = Phụ cấp * 10% 
-----• Nếu nhân viên có trình độ Tiến sĩ thì Phụ cấp = Phụ cấp * 15% 
-----• Nếu nhân viên có trình độ cử nhân thì Phụ cấp = Phụ cấp * 8% 
IF OBJECT_ID('updatephucap', 'TR') IS NOT NULL
BEGIN
    DROP TRIGGER updatephucap;
END

CREATE TRIGGER updatephucap
ON NHANVIEN
FOR INSERT, UPDATE
AS
BEGIN
    IF (EXISTS(SELECT * FROM inserted WHERE TrinhDo = N'TienSi'))
    BEGIN
        UPDATE NHANVIEN
        SET PhuCap = PhuCap + (PhuCap * 0.15)
        WHERE MaNhanVien IN (SELECT MaNhanVien FROM inserted)
        PRINT N'Cập nhật thành công thông tin Tiến Sĩ'
    END
    ELSE IF (EXISTS(SELECT * FROM inserted WHERE TrinhDo = N'ThacSi'))
    BEGIN
        UPDATE NHANVIEN
        SET PhuCap = PhuCap + (PhuCap * 0.1)
        WHERE MaNhanVien IN (SELECT MaNhanVien FROM inserted)
        PRINT N'Cập nhật thành công thông tin Thạc Sĩ'
    END
    ELSE IF (EXISTS(SELECT * FROM inserted WHERE TrinhDo = N'CuNhan'))
    BEGIN
        UPDATE NHANVIEN
        SET PhuCap = PhuCap + (PhuCap * 0.08)
        WHERE MaNhanVien IN (SELECT MaNhanVien FROM inserted)
        PRINT N'Cập nhật thành công thông tin Cử Nhân'
    END
END;
------thêm mới nhân viên có trình độ tiến sĩ
INSERT INTO NHANVIEN (MaNhanVien, HoTen, NgaySinh, GioiTinh, DiaChi, SoDienThoai, 
                      SoCCCD, TrinhDo, ChucVu, NgayVaoLam, MucLuong, PhuCap)
VALUES ('NV001', N'Nguyen Van A', '1985-05-10', N'Nam', N'Hanoi', '0123456789', 
        '012345678', N'TienSi', N'TBacSi', '2010-09-01', 15000000, 500000);
-----thêm mới nhân viên có trình độ thạc sĩ
INSERT INTO NHANVIEN (MaNhanVien, HoTen, NgaySinh, GioiTinh, DiaChi, SoDienThoai, 
                      SoCCCD, TrinhDo, ChucVu, NgayVaoLam, MucLuong, PhuCap)
VALUES ('NV002', N'Nguyen Van Accssds', '1985-05-10', N'Nam', N'Hanoi', '0123456789', 
        '012345678', N'ThacSi', N'DuocSi', '2010-09-01', 15000000, 500000);
-----thêm mới nhân viên có trình độ cử nhân
INSERT INTO NHANVIEN (MaNhanVien, HoTen, NgaySinh, GioiTinh, DiaChi, SoDienThoai, 
                      SoCCCD, TrinhDo, ChucVu, NgayVaoLam, MucLuong, PhuCap)
VALUES ('NV003', N'Nguyen Van ABCDED', '1985-05-10', N'Nam', N'Hanoi', '0123456789', 
        '012345678', N'CuNhan', N'Yta', '2010-09-01', 15000000, 500000);
---- sửa đổi trình độ nhân viên có trình độ cử nhân lên thạc sĩ
UPDATE NHANVIEN
SET TrinhDo = N'ThacSi'
WHERE MaNhanVien = 'NV003';
---thêm mới nhân viên có trình độ khác
INSERT INTO NHANVIEN (MaNhanVien, HoTen, NgaySinh, GioiTinh, DiaChi, SoDienThoai, 
                      SoCCCD, TrinhDo, ChucVu, NgayVaoLam, MucLuong, PhuCap)
VALUES ('NV004', N'Nguyen Van A', '1985-05-10', N'Nam', N'Hanoi', '0123456789', 
        '012345678', N'Khac', N'LaoCong', '2010-09-01', 15000000, 500000);