import { Module } from '@nestjs/common';
import { JobsService } from './jobs.service';
import { JobsController } from './jobs.controller';
import { MongooseModule } from '@nestjs/mongoose';
import { JobSchema } from './schemas/job.schema';
import { DirectionsModule } from 'src/directions/directions.module';

@Module({
  imports: [
    MongooseModule.forFeature([{ name: 'Job', schema: JobSchema }]),
    DirectionsModule,
  ],
  controllers: [JobsController],
  providers: [JobsService],
})
export class JobsModule {}
