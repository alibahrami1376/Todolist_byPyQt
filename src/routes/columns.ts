import { Router } from 'express';
import { prisma } from '../prisma';
const r = Router();

r.post('/projects/:id/columns', async (req, res) => {
  const { id } = req.params;
  const { title, order } = req.body;
  const col = await prisma.column.create({ data: { projectId: id, title, order } });
  res.json(col);
});

r.patch('/:id', async (req, res) => {
  const { id } = req.params;
  const col = await prisma.column.update({ where: { id }, data: req.body });
  res.json(col);
});

r.delete('/:id', async (req, res) => {
  const { id } = req.params;
  await prisma.column.delete({ where: { id } });
  res.status(204).end();
});

export default r;


