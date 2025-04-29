import { useState, useEffect } from "react";
import api from "../api";
import Sach from "../components/Sach"
import "../styles/TrangChu.css"
import "../styles/Form.css"

function TrangChu() {
    const [books, setBooks] = useState([]);
    const [tenSach, setTenSach] = useState("");
    const [theLoai, setTheLoai] = useState("");
    const [tacGia, setTacGia] = useState([{ ten_tac_gia: "" }]);
    const [nxb, setNxb] = useState("");
    const [nam_xb, setNam_xb] = useState(null);
    const [slton, setSlton] = useState(null);

    useEffect(() => {
        getBooks();
    }, []);

    const getBooks = () => {
        api
            .get("/api/sach/")
            .then((res) => res.data)
            .then((data) => {
                setBooks(data);
            })
            .catch((err) => alert(err));
    };

    const deleteBook = (id) => {
        api
            .delete(`/api/sach/delete/${id}/`)
            .then((res) => {
                if (res.status === 204) alert("Sách đã xóa!");
                else alert("Xóa sách thất bại!");
                getBooks();
            })
            .catch((error) => alert(error));
    };

    const addAuthor = () => {
        setTacGia([...tacGia, { ten_tac_gia: "" }]);
    };

    const removeAuthor = (index) => {
        const newTacGia = tacGia.filter((_, i) => i !== index);
        setTacGia(newTacGia);
    };

    const updateAuthor = (index, value) => {
        const newTacGia = [...tacGia];
        newTacGia[index].ten_tac_gia = value;
        setTacGia(newTacGia);
    };

    const createBook = (e) => {
        e.preventDefault();
        // Filter out empty author names
        const validTacGia = tacGia.filter(author => author.ten_tac_gia.trim() !== "");
        
        if (validTacGia.length === 0) {
            alert("Vui lòng nhập ít nhất một tác giả!");
            return;
        }

        const payload = { 
            dau_sach: {
                ten_sach: tenSach,
                the_loai: {
                    ten_the_loai: theLoai,
                },
                tac_gia: validTacGia,
            },
            nxb: nxb,
            nam_xb: parseInt(nam_xb),
            slton: parseInt(slton),
        };

        console.log('Sending payload:', payload);

        api
            .post("/api/sach/", payload)
            .then((res) => {
                if (res.status === 201) {
                    alert("Sách đã thêm!");
                    // Reset form
                    setTenSach("");
                    setTheLoai("");
                    setTacGia([{ ten_tac_gia: "" }]);
                    setNxb("");
                    setNam_xb(null);
                    setSlton(null);
                } else {
                    alert("Thêm sách thất bại!");
                }
                getBooks();
            })
            .catch((err) => {
                console.error('Error response:', err.response?.data);
                alert(err.response?.data?.detail || err.message || "Có lỗi xảy ra khi thêm sách");
            });
    };

    return (
        <div className="form-container">
            <h2>Danh sách sách</h2>
            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Tên sách</th>
                            <th>Thể loại</th>
                            <th>Tác giả</th>
                            <th>Nhà xuất bản</th>
                            <th>Năm xuất bản</th>
                            <th>Số lượng</th>
                            <th>Thao tác</th>
                        </tr>
                    </thead>
                    <tbody>
                        {books.map((book) => (
                            <tr key={book.id}>
                                <td>{book.dau_sach.ten_sach}</td>
                                <td>{book.dau_sach.the_loai.ten_the_loai}</td>
                                <td>{book.dau_sach.tac_gia.map(tac_gia => tac_gia.ten_tac_gia).join(", ")}</td>
                                <td>{book.nxb}</td>
                                <td>{book.nam_xb}</td>
                                <td>{book.slton}</td>
                                <td>
                                    <button 
                                        className="delete-btn"
                                        onClick={() => deleteBook(book.id)}
                                    >
                                        Xóa
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <h2>Phiếu nhập sách</h2>
            <form onSubmit={createBook}>
                <div className="form-group">
                    <label className="form-label" htmlFor="title">Tên sách:</label>
                    <input
                        type="text"
                        id="title"
                        className="form-input"
                        required
                        onChange={(e) => setTenSach(e.target.value)}
                        value={tenSach}
                        placeholder="Tên sách"
                    />
                </div>

                <div className="form-group">
                    <label className="form-label" htmlFor="theloai">Thể loại:</label>
                    <input
                        type="text" 
                        id="theloai"
                        className="form-input"
                        required
                        onChange={(e) => setTheLoai(e.target.value)}
                        value={theLoai}
                        placeholder="Thể loại"
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">Tác giả:</label>
                    <div className="authors-container">
                        {tacGia.map((author, index) => (
                            <div key={index} className="author-input-group">
                                <input
                                    type="text"
                                    className="author-input"
                                    required
                                    onChange={(e) => updateAuthor(index, e.target.value)}
                                    value={author.ten_tac_gia}
                                    placeholder="Tên tác giả"
                                />
                                {index === tacGia.length - 1 && (
                                    <button 
                                        type="button" 
                                        className="add-author-btn"
                                        onClick={addAuthor}
                                    >
                                        +
                                    </button>
                                )}
                                {index > 0 && (
                                    <button 
                                        type="button" 
                                        className="remove-author-btn"
                                        onClick={() => removeAuthor(index)}
                                    >
                                        -
                                    </button>
                                )}
                            </div>
                        ))}
                    </div>
                </div>

                <div className="form-group">
                    <label className="form-label" htmlFor="nxb">Nhà xuất bản:</label>
                    <input
                        type="text"
                        id="nxb"
                        className="form-input"
                        required
                        onChange={(e) => setNxb(e.target.value)}
                        value={nxb}
                        placeholder="Nhà xuất bản"
                    />
                </div>

                <div className="form-group">
                    <label className="form-label" htmlFor="namxb">Năm xuất bản:</label>
                    <input
                        type="number"
                        id="namxb"
                        className="form-input"
                        required
                        onChange={(e) => setNam_xb(e.target.value)}
                        value={nam_xb}
                        placeholder="Năm xuất bản"
                    />
                </div>

                <div className="form-group">
                    <label className="form-label" htmlFor="slton">Số lượng nhập:</label>
                    <input
                        type="number"
                        id="slton"
                        className="form-input"
                        required
                        onChange={(e) => setSlton(e.target.value)}
                        value={slton}
                        placeholder="Số lượng nhập"
                    />
                </div>

                <button type="submit" className="submit-btn">Thêm sách mới</button>
            </form>
        </div>
    );
}

export default TrangChu;