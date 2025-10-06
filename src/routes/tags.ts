import { Router } from 'express';
import { prisma } from '../prisma';
const r = Router();

r.post('/', async (req, res) => {
  const tag = await prisma.tag.create({ data: req.body });
  res.json(tag);
});

r.get('/', async (_req, res) => {
  res.json(await prisma.tag.findMany({ orderBy: { name: 'asc' } }));
});

r.post('/steps/:id/tags', async (req, res) => {
  const { id } = req.params;
  const { tagId } = req.body;
  const link = await prisma.taskTag.create({ data: { stepId: id, tagId } });
  res.json(link);
});

r.delete('/steps/:id/tags/:tagId', async (req, res) => {
  const { id, tagId } = req.params as { id: string; tagId: string };
  await prisma.taskTag.delete({ where: { stepId_tagId: { stepId: id, tagId } } });
  res.status(204).end();
});

export default r;


