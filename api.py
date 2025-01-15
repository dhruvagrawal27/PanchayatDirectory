from flask import Flask, jsonify, request, render_template
import psycopg2
import pandas as pd
from psycopg2.extras import execute_values
from typing import Dict, List
import json

# Database connection parameters
DB_PARAMS = {
    "user": "postgres.npfjzmvmpgdinktkniqn",
    "password": "dhruv@27",
    "host": "aws-0-ap-south-1.pooler.supabase.com",
    "port": "6543",
    "dbname": "postgres"
}

app = Flask(__name__)

# Helper function to connect to the database
def get_db_connection():
    return psycopg2.connect(**DB_PARAMS)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/states", methods=["GET"])
def get_states():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to get distinct StateCode and StateName
        query = """
        SELECT DISTINCT "StateCode", "StateName"
        FROM "panchayat_members"
        LIMIT 100;
        """
        
        cursor.execute(query)
        states = [dict(StateCode=row[0], StateName=row[1]) for row in cursor.fetchall()]
        
        return jsonify(states)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

@app.route("/api/districts/<StateCode>", methods=["GET"])
def get_districts(StateCode):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to get distinct DistrictCode and DistrictName for a given StateCode
        query = """
        SELECT DISTINCT "DistrictCode", "DistrictName"
        FROM "panchayat_members"
        WHERE "StateCode" = %s
        LIMIT 1000;
        """
        
        cursor.execute(query, (StateCode,))
        districts = [dict(DistrictCode=row[0], DistrictName=row[1]) for row in cursor.fetchall()]
        
        return jsonify(districts)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()


@app.route("/api/taluks/<DistrictCode>", methods=["GET"])
def get_taluks(DistrictCode):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to get distinct BlockCode and BlockName for a given DistrictCode
        query = """
        SELECT DISTINCT "BlockCode", "BlockName"
        FROM "panchayat_members"
        WHERE "DistrictCode" = %s
        LIMIT 100;
        """
        
        cursor.execute(query, (DistrictCode,))
        taluks = [dict(BlockCode=row[0], BlockName=row[1]) for row in cursor.fetchall()]
        
        return jsonify(taluks)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

@app.route("/api/villages/<taluk_code>", methods=["GET"])
def get_villages(taluk_code):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to get distinct GramPanchayatCode and GramPanchayatName for a given taluk_code
        query = """
        SELECT DISTINCT "GramPanchayatCode", "GramPanchayatName"
        FROM "panchayat_members"
        WHERE "BlockCode" = %s
        LIMIT 100;
        """
        
        cursor.execute(query, (taluk_code,))
        villages = [dict(GramPanchayatCode=row[0], GramPanchayatName=row[1]) for row in cursor.fetchall()]
        
        return jsonify(villages)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()


@app.route("/api/members", methods=["GET"])
def get_members():
    try:
        village_code = request.args.get("GramPanchayatCode")
        connection = get_db_connection()
        cursor = connection.cursor()

        if village_code:
            query = """
            SELECT "ElectedName" AS "Name", "DesignationName", "MobileNumber", "EmailId", 
                   "GramPanchayatName", "BlockName", "DistrictName", "StateName" 
            FROM "panchayat_members" 
            WHERE "GramPanchayatCode" = %s;
            """
            cursor.execute(query, (village_code,))
        else:
            query = """
            SELECT "ElectedName", "DesignationName", "MobileNumber", "EmailId", "GramPanchayatName", 
                   "BlockName", "DistrictName", "StateName" 
            FROM "panchayat_members";
            """
            cursor.execute(query)

        members = [
            dict(
                ElectedName=row[0],
                DesignationName=row[1],
                MobileNumber=row[2],
                EmailId=row[3],
                GramPanchayatName=row[4],
                BlockName=row[5],
                DistrictName=row[6],
                StateName=row[7]
            ) for row in cursor.fetchall()
        ]
        return jsonify(members)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

@app.route("/api/members/add", methods=["POST"])
def add_member():
    try:
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if village exists
        cursor.execute("""SELECT * FROM "panchayat_members" WHERE "GramPanchayatCode" = %s LIMIT 1;""", (data["GramPanchayatCode"],))
        village_data = cursor.fetchone()
        if not village_data:
            return jsonify({"success": False, "message": "Invalid village code."}), 400

        # Insert new member
        insert_query = """
        INSERT INTO "panchayat_members" (
            "StateCode", "StateName", "DistrictCode", "DistrictName", 
            "BlockCode", "BlockName", "GramPanchayatCode", "GramPanchayatName", 
            "ElectedName", "MobileNumber", "EmailId", "DesignationName"
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(
            insert_query,
            (
                village_data[1], village_data[2], village_data[3], village_data[4],
                village_data[5], village_data[6], village_data[7], village_data[8],
                data["ElectedName"], data["MobileNumber"], data["EmailId"], data["DesignationName"]
            )
        )
        connection.commit()
        return jsonify({"success": True, "message": "Member added successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

@app.route("/api/search")
def search():
    search_term = request.args.get("term", "").lower()
    if not search_term or len(search_term) < 2:
        return jsonify({"results": []})

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
        SELECT DISTINCT "StateCode", "StateName", "DistrictCode", "DistrictName", "BlockCode", "BlockName", 
        "GramPanchayatCode", "GramPanchayatName"
        FROM "panchayat_members"
        WHERE LOWER("StateName") LIKE %s OR LOWER("DistrictName") LIKE %s 
        OR LOWER("BlockName") LIKE %s OR LOWER("GramPanchayatName") LIKE %s
        LIMIT 10;
        """
        cursor.execute(query, tuple([f"%{search_term}%"] * 4))
        results = [
            dict(
                StateCode=row[0],
                StateName=row[1],
                DistrictCode=row[2],
                DistrictName=row[3],
                BlockCode=row[4],
                BlockName=row[5],
                GramPanchayatCode=row[6],
                GramPanchayatName=row[7]
            ) for row in cursor.fetchall()
        ]
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"results": [], "error": str(e)}), 500
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
