import React from "react";
import "../styles/Sach.css"

function Sach({ book, onDelete }) {
    return (
        <div className="sach-container">
            <p className="sach-title">{book.dau_sach.ten_sach}</p>
            <p className="sach-the-loai">{book.dau_sach.the_loai.ten_the_loai}</p>
            <p className="sach-tac-gia">
                {Array.isArray(book.dau_sach.tac_gia) 
                    ? book.dau_sach.tac_gia.map(tac_gia => tac_gia.ten_tac_gia).join(", ")
                    : "Không có tác giả"}
            </p>
            <p className="sach-nxb">{book.nxb}</p>
            <p className="sach-nam-xb">{book.nam_xb}</p>
            <p className="sach-slton">{book.slton}</p>
            <button className="delete-button" onClick={() => onDelete(book.id)}>
                Delete
            </button>
        </div>
    );
}

export default Sach;