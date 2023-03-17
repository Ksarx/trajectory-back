import { Module } from '@nestjs/common';
import { JobsModule } from './jobs/jobs.module';
import { DirectionsModule } from './directions/directions.module';
import { MongooseModule } from '@nestjs/mongoose';
import { ConfigModule } from '@nestjs/config';

@Module({
  imports: [
    ConfigModule.forRoot(),
    MongooseModule.forRoot(process.env.DB_URL),
    JobsModule,
    DirectionsModule,
  ],
  controllers: [],
  providers: [],
})
export class AppModule {}
