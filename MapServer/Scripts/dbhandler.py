import sqlite3
import time
class DBHandler:
    conn = ""
    cur = ""

    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.db_init()

    # 数据库配置
    def db_init(self):
        try:
            self.cur.execute("""
            CREATE TABLE Zone (
            id TEXT PRIMARY KEY,
            updatetime TEXT,
            name TEXT
            )
            """)
        except:
            pass
        try:
            self.cur.execute("""
            CREATE TABLE Map (
            id TEXT PRIMARY KEY,
            updatetime TEXT,
            name TEXT,
            zone TEXT,
            offset TEXT,
            pgm TEXT,
            yaml TEXT,
            md5 TEXT
            )
            """)
        except:
            pass
        try:
            self.cur.execute("""
            CREATE TABLE AgvPoint (
            id TEXT PRIMARY KEY,
            updatetime TEXT,
            name TEXT,
            zone TEXT,
            type Integer,
            pose TEXT
            )
            """)
        except:
            pass
        try:
            self.cur.execute("""
            CREATE TABLE ArmPoint (
            id TEXT PRIMARY KEY,
            updatetime TEXT,
            name TEXT,
            zone TEXT,
            type Integer,
            pose TEXT
            )
            """)
        except:
            pass
        try:
            self.cur.execute("""
            CREATE TABLE Wall (
            id TEXT PRIMARY KEY,
            updatetime TEXT,
            name TEXT,
            zone TEXT,
            poses TEXT
            )
            """)
        except:
            pass
        try:
            self.cur.execute("""
            CREATE TABLE Track (
            id TEXT PRIMARY KEY,
            updatetime TEXT,
            name TEXT,
            zone TEXT,
            type Integer,
            poses TEXT
            )
            """)
        except:
            pass

    # 空间表    
    def zone_get(self):
        self.cur.execute("""
            SELECT * FROM Zone;
        """)
        return self.cur.fetchall()

    def zone_edit(self, id, name):
        try:
            self.cur.execute("""
                INSERT INTO Zone (id,updatetime,name)
                VALUES (?,?,?)
            """, (id,str(int(time.time()*1000)),name))
        except sqlite3.Error as e:
            self.cur.execute("""
                UPDATE Zone
                SET updatetime =?, name = ?
                WHERE id = ?
            """, (str(int(time.time()*1000)), name, id))
        self.conn.commit()

    def zone_delete(self, id):
        self.cur.execute("""
            DELETE FROM Zone
            WHERE id = ?
        """, (id,))
        self.conn.commit()

    # 地图表
    def map_get(self):
        self.cur.execute("""
            SELECT * FROM Map;
        """)
        return self.cur.fetchall()

    def map_edit(self, id, name, zone, offset, pgm, yaml, md5):
        try:
            self.cur.execute("""
                INSERT INTO Map (id,updatetime,name,zone,offset,pgm,yaml,md5)
                VALUES (?,?,?,?,?,?,?,?)
            """, (id,str(int(time.time()*1000)),name,zone,offset,pgm,yaml,md5))
        except sqlite3.Error as e:
            self.cur.execute("""
                UPDATE Map
                SET updatetime = ?, name = ?, zone = ?, offset = ?, pgm = ?, yaml = ?, md5 = ?
                WHERE id = ?
            """, (str(int(time.time()*1000)),name,zone,offset,pgm,yaml,md5,id))
        self.conn.commit()

    def map_delete(self, id):
        self.cur.execute("""
            DELETE FROM Map
            WHERE id = ?
        """, (id,))
        self.conn.commit()

    # AGV点表
    def agvpoint_get(self):
        self.cur.execute("""
            SELECT * FROM AgvPoint;
        """)
        return self.cur.fetchall()

    def agvpoint_edit(self, id, name, zone, type, pose):
        try:
            self.cur.execute("""
                INSERT INTO AgvPoint (id,updatetime,name,zone,type,pose)
                VALUES (?,?,?,?,?,?)
            """, (id,str(int(time.time()*1000)),name,zone,type,pose))
        except sqlite3.Error as e:
            self.cur.execute("""
                UPDATE AgvPoint
                SET updatetime = ?, name = ?, zone = ?, type = ?, pose = ?
                WHERE id = ?
            """, (str(int(time.time()*1000)),name,zone,type,pose,id))
        self.conn.commit()

    def agvpoint_delete(self, id):
        self.cur.execute("""
            DELETE FROM AgvPoint
            WHERE id = ?
        """, (id,))
        self.conn.commit()

    # 机械臂点表
    def armpoint_get(self):
        self.cur.execute("""
            SELECT * FROM ArmPoint;
        """)
        return self.cur.fetchall()

    def armpoint_edit(self, id, name, zone, type, pose):
        try:
            self.cur.execute("""
                INSERT INTO ArmPoint (id,updatetime,name,zone,type,pose)
                VALUES (?,?,?,?,?,?)
            """, (id,str(int(time.time()*1000)),name,zone,type,pose))
        except sqlite3.Error as e:
            self.cur.execute("""
                UPDATE ArmPoint
                SET updatetime = ?, name = ?, zone = ?, type = ?, pose = ?
                WHERE id = ?
            """, (str(int(time.time()*1000)),name,zone,type,pose,id))
        self.conn.commit()

    def armpoint_delete(self, id):
        self.cur.execute("""
            DELETE FROM ArmPoint
            WHERE id = ?
        """, (id,))
        self.conn.commit()

    # 虚拟墙表
    def wall_get(self):
        data = ""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM Wall;
            """)
            data = cursor.fetchall()
        except sqlite3.Error as e:
            self.conn.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()
        return data

    def wall_edit(self, id, name, zone, poses):
        try:
            cursor = self.conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO Wall (id,updatetime,name,zone,poses)
                    VALUES (?,?,?,?,?)
                """, (id,str(int(time.time()*1000)),name,zone,poses))
            except sqlite3.Error as e:
                cursor.execute("""
                    UPDATE Wall
                    SET updatetime = ?, name = ?, zone = ?, poses = ?
                    WHERE id = ?
                """, (str(int(time.time()*1000)),name,zone,poses,id))
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()

    def wall_delete(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM Wall
                WHERE id = ?
            """, (id,))
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()



    # 轨迹表
    def track_get(self):
        self.cur.execute("""
            SELECT * FROM Track;
        """)
        return self.cur.fetchall()

    def track_edit(self, id, name, zone, type, poses):
        try:
            self.cur.execute("""
                INSERT INTO Track (id,updatetime,name,zone,type,poses)
                VALUES (?,?,?,?,?,?)
            """, (id,str(int(time.time()*1000)),name,zone,type,poses))
        except sqlite3.Error as e:
            self.cur.execute("""
                UPDATE Track
                SET updatetime = ?, name = ?, zone = ?, type = ?, poses = ?
                WHERE id = ?
            """, (str(int(time.time()*1000)),name,zone,type,poses,id))
        self.conn.commit()

    def track_delete(self, id):
        self.cur.execute("""
            DELETE FROM Track
            WHERE id = ?
        """, (id,))
        self.conn.commit()

if __name__ == '__main__':
    # 使用示例
    db = DBHandler("my_database.db")
    db.db_init()