import { Router } from 'express';
import { prisma } from '../prisma';

const r = Router();

r.post('/', async (req, res) => {
  const data = req.body;
  const project = await prisma.project.create({ data });
  res.json(project);
});

r.get('/', async (_req, res) => {
  const projects = await prisma.project.findMany({ orderBy: { createdAt: 'desc' } });
  res.json(projects);
});

r.get('/:id', async (req, res) => {
  const { id } = req.params;
  const project = await prisma.project.findUnique({
    where: { id },
    include: { columns: { orderBy: { order: 'asc' } }, steps: true },
  });
  res.json(project);
});

r.patch('/:id', async (req, res) => {
  const { id } = req.params;
  const project = await prisma.project.update({ where: { id }, data: req.body });
  res.json(project);
});

r.delete('/:id', async (req, res) => {
  const { id } = req.params;
  await prisma.project.delete({ where: { id } });
  res.status(204).end();
});

export default r;


