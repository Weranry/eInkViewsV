import json
import os
from datetime import datetime
from modules.common_timezone import now_in_timezone
from modules.errors.errors import ParamError

class ScheduleFetcher:
    def __init__(self, json_name='course_schedule'):
        self.plugin_dir = os.path.dirname(os.path.dirname(__file__))
        self.json_path = os.path.join(self.plugin_dir, 'assets', 'course', f'{json_name}.json')
        
        if not os.path.exists(self.json_path):
            raise ParamError(f"课程表文件 {json_name}.json 不存在")
            
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except Exception as e:
            raise ParamError(f"解析课程表失败: {str(e)}")

    def fetch(self, tz=None):
        current_date = now_in_timezone(tz)
        
        try:
            semester_start = datetime.strptime(
                self.data['semesterStartDate'], 
                '%Y-%m-%d'
            ).replace(tzinfo=current_date.tzinfo)
        except Exception as e:
            raise ParamError(f"学期日期格式错误: {str(e)}")

        # 计算周数 (周一为一周开始)
        delta = current_date - semester_start
        week_number = (delta.days // 7) + 1
        day_of_week = current_date.isoweekday() # 1-7

        courses = self.data.get('courses', [])
        # 5节课
        today_schedule = [{'lesson': i, 'course': {}} for i in range(1, 6)]

        for course in courses:
            for classroom in course.get('classroom', []):
                if (classroom.get('dayOfWeek') == day_of_week and 
                    week_number in classroom.get('week', [])):
                    lesson_idx = classroom.get('lesson', 1) - 1
                    if 0 <= lesson_idx < 5:
                        today_schedule[lesson_idx]['course'] = {
                            'name': course.get('courseName', ''),
                            'room': classroom.get('room', ''),
                            'teacher': course.get('teacher', '')
                        }

        date_info = {
            'todayDate': current_date.strftime('%Y-%m-%d'),
            'weekNumber': week_number,
            'dayOfWeek': ['一', '二', '三', '四', '五', '六', '日'][day_of_week - 1]
        }

        formatted_schedule = {
            f'course{i+1}': today_schedule[i]['course'] for i in range(5)
        }

        return {'dateInfo': date_info, 'schedule': formatted_schedule}
