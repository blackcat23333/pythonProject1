import datetime
import shutil

# 需要备份的文件路径和目标备份目录
source_path = 'C:\\Users\\Administrator\\Desktop\\1'
backup_path = 'C:\\Users\\Administrator\\Desktop\\2'

# 生成备份文件名
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
backup_filename = f'backup_{timestamp}.tar.gz'

# 执行备份
shutil.make_archive(f'{backup_path}/{backup_filename}', 'gztar', source_path)