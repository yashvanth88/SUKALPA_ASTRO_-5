import { BrowserRouter, Routes, Route } from "react-router-dom";
import SignupPage from './pages/Signup';
import LoginPage from './pages/Login';
import VerifyEmailPage from './pages/VerifyEmail';
import DashboardPage from './pages/Dashboard';

function App() {
    return( 
        <div className="min-h-full h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full space-y-8">
                <BrowserRouter>
                    <Routes>
                        <Route path="/" element={<LoginPage/>} />
                        <Route path="/signup" element={<SignupPage/>} />
                        <Route path="/dashboard" element={<DashboardPage/>} />
                        <Route path="/verify-email" element={<VerifyEmailPage/>} />
                    </Routes>
                </BrowserRouter>
            </div>
        </div>  
    )
}

export default App;