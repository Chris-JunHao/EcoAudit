import express from 'express';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

// 获取当前文件的路径
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = 3000;

// 提供静态文件目录
app.use(express.static('public'));

// 根路径响应
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// 获取指定省份的河流文件名
app.get('/api/getRivers', (req, res) => {
  const province = req.query.province;  // 获取省份参数
  const provincePath = decodeURI(path.join(__dirname, 'public', 'province', province));

  // 输出路径用于调试
  console.log(`Attempting to read from: ${provincePath}`);

  // 检查目录是否存在
  if (!fs.existsSync(provincePath)) {
    console.error(`Directory not found: ${provincePath}`);
    return res.status(404).json({ error: 'Province not found' });
  }

  // 读取目录中的文件
  fs.readdir(provincePath, (err, files) => {
    if (err) {
      console.error(`Failed to read directory: ${provincePath}`, err);
      return res.status(500).json({ error: 'Failed to read directory' });
    }

    // 过滤出 .csv 文件
    const csvFiles = files.filter(file => file.endsWith('.csv'));

    // 将文件名返回给前端
    res.json(csvFiles);
  });
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
