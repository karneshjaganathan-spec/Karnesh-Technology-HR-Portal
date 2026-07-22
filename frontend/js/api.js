const API = "http://127.0.0.1:5000/api";

class HRAPI {

    // ==========================
    // GET
    // ==========================
    static async get(endpoint) {

        try {

            const response = await fetch(API + endpoint, {
                method: "GET",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                }
            });

            return await response.json();

        } catch (error) {

            console.error(error);

            return {
                success: false,
                message: "Server connection failed."
            };
        }

    }

    // ==========================
    // POST
    // ==========================
    static async post(endpoint, data) {

        try {

            const response = await fetch(API + endpoint, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            return await response.json();

        } catch (error) {

            console.error(error);

            return {
                success: false,
                message: "Server connection failed."
            };

        }

    }

    // ==========================
    // PUT
    // ==========================
    static async put(endpoint, data) {

        try {

            const response = await fetch(API + endpoint, {
                method: "PUT",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            return await response.json();

        } catch (error) {

            console.error(error);

            return {
                success: false,
                message: "Server connection failed."
            };

        }

    }

    // ==========================
    // DELETE
    // ==========================
    static async delete(endpoint) {

        try {

            const response = await fetch(API + endpoint, {
                method: "DELETE",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                }
            });

            return await response.json();

        } catch (error) {

            console.error(error);

            return {
                success: false,
                message: "Server connection failed."
            };

        }

    }

}