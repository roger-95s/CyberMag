// import { useState, useEffect } from "react";
import Header from "../components/Header";
import ReportCard from "../components/ReportCard.jsx";


function PostPage() {
    return (
        <div className="min-h-screen bg-white dark:bg-[#0a0f1a] text-gray-900 dark:text-gray-100 transition-colors duration-500">
            <Header />
            <h1 className="text-4xl font-bold text-center my-8">All Posts</h1>
            <ReportCard />
        </div>
    );
}

export default PostPage;
