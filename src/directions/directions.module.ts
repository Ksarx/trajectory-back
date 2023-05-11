import { Module } from '@nestjs/common';
import { DirectionsService } from './directions.service';
import { DirectionsController } from './directions.controller';
import { MongooseModule } from '@nestjs/mongoose';
import { DirectionSchema } from './schemas/direction.schema';

@Module({
  imports: [
    MongooseModule.forFeature([{ name: 'Direction', schema: DirectionSchema }]),
  ],
  controllers: [DirectionsController],
  providers: [DirectionsService],
  exports: [DirectionsService],
})
export class DirectionsModule {}
