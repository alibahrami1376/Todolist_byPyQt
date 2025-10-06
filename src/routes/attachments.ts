import { Router } from 'express';
import { prisma } from '../prisma';
const r = Router();

r.post('/steps/:id/attachments', async (req, res) => {
  const { id } = req.params;
  const { fileUrl, type } = req.body;
  const a = await prisma.attachment.create({ data: { stepId: id, fileUrl, type } });
  res.json(a);
});

r.get('/steps/:id/attachments', async (req, res) => {
  const { id } = req.params;
  res.json(await prisma.attachment.findMany({ where: { stepId: id }, orderBy: { createdAt: 'desc' } }));
});

r.delete('/:id', async (req, res) => {
  const { id } = req.params;
  await prisma.attachment.delete({ where: { id } });
  res.status(204).end();
});

export default r;


