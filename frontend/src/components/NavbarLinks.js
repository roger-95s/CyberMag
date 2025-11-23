function NavLink() {
    return (
        <div className="hidden md:flex gap-6 text-sm font-medium text-gray-700 dark:text-gray-300">
            <div class="flex space-x-4">
                {/* Current: "bg-gray-950/50 text-white", Default: "text-gray-300 hover:bg-white/5 hover:text-white" */}
                <a href="/" aria-current="page" class="rounded-md bg-gray-950/50 px-3 py-2 text-sm font-medium text-white">Home</a>
                <a href="/posts/" class="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-white/5 hover:text-white">Posts</a>
                <a href="/about/" class="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-white/5 hover:text-white">About us</a>
            </div>
        </div>
    );
}

export { NavLink };