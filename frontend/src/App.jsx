import react from "react"
import { BrowserRouter, Routes, Route, Navigate} from "react-router-dom";
import TrangChu from "./pages/TrangChu";
import DangNhap from "./pages/DangNhap";
import DangKy from "./pages/DangKy";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";

function DangXuat() {
  localStorage.clear();
  return <Navigate to="/dang-nhap" />;
}

function DangKy_DangXuat() {
  localStorage.clear();
  return <DangKy />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProtectedRoute>
          <TrangChu />
        </ProtectedRoute>
        } 
        />
        <Route path="/dang-nhap" element={<DangNhap />} />
        <Route path="/dang-ky" element={<DangKy_DangXuat />} />
        <Route path="/dang-xuat" element={<DangXuat />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App;
